from django.shortcuts import get_object_or_404
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
    

class RecipeSerializer(ModelSerializer):
    author = UserSerializer(default=serializers.CurrentUserDefault())
    ingredients = IngredientRecipeSerializer(many=True, read_only=True, partial=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text', 'cooking_time', 'ingredients')

    def update(self, instance, validated_data):
        self.instance.ingredients.all().delete()
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredients.objects.create(
                recipe=self.instance,
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount']
            )
            recipe_ingredient.save()
        super().update(instance, validated_data)
        return instance

    def create(self, validated_data):
        """
        Модифицированный create для сохранения связанных записей
        Рецепт содается, только при наличии всех ингедиентов
        !!!Доделть теги!!!
        """
        ingredients = validated_data.pop('ingredients')
        validated_data['author'] = self.context['request'].user
        recipe = super().create(validated_data)
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount']
            )
        return recipe

    def validate(self, data):
        ingredients_internal = self.initial_data['ingredients']
        tags = data['tags']
        for tag in tags:
            if not Tag.objects.filter(pk=tag.pk).exists():
                raise serializers.ValidationError(f'Тэга id={tag} нет')
        for ingredient in ingredients_internal:
            if not Ingredient.objects.filter(pk=ingredient['id']).exists():
                raise serializers.ValidationError(f'Нет ингредиента id={ingredient["id"]}')

        validated_data =super().validate(data)
        validated_data['ingredients'] = ingredients_internal
        return validated_data


