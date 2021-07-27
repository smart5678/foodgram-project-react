from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Recipe, Ingredient, RecipeIngredients
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

    def to_internal_value(self, data):
        """Добавляем работу с полями ингридиентов"""
        ingredients_internal = data.pop('ingredients')
        validated_data =super().validate(data)
        validated_data['ingredients'] = ingredients_internal
        return data

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
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        validated_data['author'] = self.context['request'].user
        recipe = Recipe(**validated_data)
        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(
                RecipeIngredients(
                    recipe=recipe,
                    ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                    amount=ingredient['amount']
                )
            )
        recipe.save()
        RecipeIngredients.objects.bulk_create(recipe_ingredients)
        recipe.tags.set(tags)
        return recipe
