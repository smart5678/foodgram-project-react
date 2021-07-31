from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from users.serializers import UserSerializer

USER = get_user_model()

class SubscribedRecipeSerializer(RecipeSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscriberSerializer(UserSerializer):
    recipes = SubscribedRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = USER
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
        )
