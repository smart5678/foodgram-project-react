from django.shortcuts import get_object_or_404
import base64

from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from .models import Recipe, Ingredient, RecipeIngredients, Tag
from users.serializers import UserSerializer


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'ingredient', 'amount')

    def to_representation(self, instance):
        """
        Делаем отображение полей ингредиента в отображение рецепта плоским
        Будет также переписан id ингредиента вместо id RecipeIngredient
        """
        representation = super().to_representation(instance)
        ingredient_representation = representation.pop('ingredient')
        for key in ingredient_representation:
            representation[key] = ingredient_representation[key]
        return representation


class RecipeIngredientsSerializer(ModelSerializer):

    class Meta:
        model = RecipeIngredients
        fields = '__all__'


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    """
    В update и create дополнительно обновляются связанные модели ингредиентов.
    """
    author = UserSerializer()
    ingredients = IngredientRecipeSerializer(many=True, read_only=True, partial=False)
    tags = TagSerializer(many=True, read_only=True, partial=False)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if user.is_authenticated and user.favorites.filter(favorite_recipe=recipe):
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if user.is_authenticated and user.buyer.filter(recipe=recipe):
            return True
        return False

    def update(self, instance, validated_data):
        ingredient_list = []
        for ingredient in validated_data.pop('ingredients'):
            ingredient_list.append({
                'recipe': self.instance.id,
                'ingredient': ingredient['ingredient']['id'],
                'amount': ingredient['ingredient']['amount'],
            })

        ingredient_serializer = RecipeIngredientsSerializer(data=ingredient_list, many=True)
        recipe_serializer = SimpleRecipeSerializer(data=validated_data, partial=True)

        valid = ingredient_serializer.is_valid()
        valid &= recipe_serializer.is_valid()
        if valid:
            super().update(instance, validated_data)
            self.instance.ingredients.all().delete()
            ingredient_serializer.save()
        else:
            raise serializers.ValidationError(
                {'detail': [
                            {f'Ошибки в ингредиентах': ingredient_serializer.errors or 'Нет ошибок'},
                            {f'Ошибки в рецепте {instance.name}': recipe_serializer.errors or 'Нет ошибок'}
                ]}
            )
        return instance

    def create(self, validated_data):
        """
        Модифицированный create для сохранения связанных записей
        Рецепт содается, только при наличии всех ингедиентов
        """
        ingredients = validated_data.pop('ingredients')
        validated_data['author'] = self.context['request'].user
        recipe = super().create(validated_data)
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(Ingredient, pk=ingredient['ingredient']['id']),
                amount=ingredient['ingredient']['amount']
            )
        return recipe

    def to_internal_value(self, data):
        """
        Возвращает список ингредиентов к формату сериализатора модели ингредиентов
        Декодирует картинку из base64, отдает путь в image модели.
        """
        internal_data = data
        if self.context.get('request').method in ['PUT', 'POST']:
            image = internal_data.pop('image')
            format, imgstr = image.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            image_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            internal_data['image'] = image_file

        ingredients = data.pop('ingredients')
        ingredients_internal = []
        for ingredient in ingredients:
            ingredients_internal.append({"ingredient": ingredient})
        internal_data['ingredients'] = ingredients_internal

        return internal_data

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text', 'cooking_time', 'ingredients', 'image', 'is_favorited', 'is_in_shopping_cart')


class SimpleRecipeSerializer(UserSerializer):
    """
    Используется для спсиков избранного и корзины
    С его помощью валидируются несвязанные поля.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
            'author',
            'text'
        )
