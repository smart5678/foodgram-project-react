from django.shortcuts import get_object_or_404
import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
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
        Добавляем поля ингредиента в отображение рецепта
        Будет также переписан id ингредиента вместо id RecipeIngredient
        Можно изменить, если в IngredientSerializer.Meta.fields убрать id
        """
        representation = super().to_representation(instance)
        ingredient_representation = representation.pop('ingredient')
        for key in ingredient_representation:
            representation[key] = ingredient_representation[key]
        return representation


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

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text', 'cooking_time', 'ingredients', 'image')

    def update(self, instance, validated_data):
        self.instance.ingredients.all().delete()
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredients.objects.create(
                recipe=self.instance,
                ingredient=get_object_or_404(Ingredient, pk=ingredient['ingredient']['id']),
                amount=ingredient['ingredient']['amount']
            )
            recipe_ingredient.save()
        super().update(instance, validated_data)
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


