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

    def to_representation(self, instance):
        """
        Добавляем поля ингредиента в отображение рецепта
        Будет также переписан id ингредиента вместо id RecipeIngredient
        Можно изменить, если в IngredientSerializer.Meta.fields убрать id
        """
        params = self.context.get('request').query_params
        recipes_limit = params.get('recipes_limit')
        representation = super().to_representation(instance)
        recipes = representation.pop('recipes', [])
        if recipes_limit and len(recipes) >= int(recipes_limit):
            representation['recipes'] = recipes[:int(recipes_limit)]
        else:
            representation['recipes'] = recipes
        return representation
