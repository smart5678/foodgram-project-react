from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import SimpleRecipeSerializer
from users.serializers import UserSerializer

USER = get_user_model()


class SubscriberSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()

    def get_recipes(self, author):
        """
        Огрничиваем количство рецептов по параметру recipes_limit
        :param author: пользователь для которого берутся рецепты
        :return: сериализованные данные рецептов автора
        """
        recipes_limit = self.context.get('request').query_params.get('recipes_limit')
        if recipes_limit is not None:
            query = Recipe.objects.filter(author=author)[:int(recipes_limit)]
        else:
            query = Recipe.objects.filter(author=author)
        serializer = SimpleRecipeSerializer(query, many=True)
        return serializer.data

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


class FavoriteSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()

    def get_recipes(self, author):
        """
        Огрничиваем количство рецептов по параметру recipes_limit
        :param author: пользователь для которого берутся рецепты
        :return: сериализованные данные рецептов автора
        """
        recipes_limit = self.context.get('request').query_params.get('recipes_limit')
        if recipes_limit is not None:
            query = Recipe.objects.filter(author=author)[:int(recipes_limit)]
        else:
            query = Recipe.objects.filter(author=author)
        serializer = SimpleRecipeSerializer(query, many=True)
        return serializer.data

