from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Recipe, Ingredient, RecipeIngredients
from users.serializers import UserSerializer






class IngredientRecipeSerializer(ModelSerializer):
    ingredient = serializers.IngridientListingField(read_only=True)

    class Meta:
        model = RecipeIngredients
        fields = ('ingredient', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

