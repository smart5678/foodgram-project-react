from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Recipe, Ingredient, RecipeIngredients
from users.serializers import UserSerializer


class IngredientRecipeSerializer(ModelSerializer):

    class Meta:
        model = RecipeIngredients
        fields = '__all__'


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
