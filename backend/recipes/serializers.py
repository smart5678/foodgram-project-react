from rest_framework import serializers
from rest_framework.generics import get_object_or_404
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
        Будет также переписан id ингредиента вместо id ReceptIngredient
        """
        representation = super().to_representation(instance)
        ingredient_representation = representation.pop('ingredient')
        for key in ingredient_representation:
            representation[key] = ingredient_representation[key]
        return representation
    
    # def to_internal_value(self, data):
    #     """Выносим поля ингредиента в отдельный словарь"""
    #     print(self.initial_data)
    #     ingredient_internal = {}
    #     for key in IngredientSerializer.Meta.fields:
    #         if key in data:
    #             ingredient_internal[key] = data.pop[key]
    #     internal = super().to_internal_value(data)
    #     internal['ingredient'] = ingredient_internal
    #     return internal
    #
    # def update(self, instance, validated_data):
    #     """Обновление рецепта и количества ингредиентов"""
    #     ingredient_data = validated_data.pop('ingredients')
    #     print(ingredient_data)
    #     super().update(instance, validated_data)
    #
    #     ingredient = instance.ingredient
    #     for attr, value in ingredient_data.items():
    #
    #         setattr(ingredient, attr, value)
    #     ingredient.save()
        

class RecipeSerializer(ModelSerializer):
    author = UserSerializer(default=serializers.CurrentUserDefault())
    ingredients = IngredientRecipeSerializer(many=True, read_only=True, partial=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text', 'cooking_time', 'ingredients')

    def to_internal_value(self, data):
        """Добавляем работу с полями ингридиентов"""
        ingredients_internal = {}
        ingredients_internal = data.pop('ingredients')
        print(ingredients_internal)
        self.instance.ingredients.all().delete()

        for ingredient_internal in ingredients_internal:
            recipe_ingredient = RecipeIngredients.objects.create(
                recipe=self.instance,
                ingredient=get_object_or_404(Ingredient, pk=ingredient_internal['id']),
                amount=ingredient_internal['amount']
            )
            recipe_ingredient.save()
        return data

    def update(self, instance, validated_data):
        print(validated_data)
        super().update(instance, validated_data)
        return instance