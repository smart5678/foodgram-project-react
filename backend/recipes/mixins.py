from django.db.models import Model
from rest_framework import status, serializers
from rest_framework.response import Response

from recipes.serializers import RecipeIngredientsSerializer, \
    SimpleRecipeSerializer


def set_action(
        self, request, recipe_pk,
        acted_serializer=None, response_serializer=None,
        acted_model=None, response_model=None,
        follow=None, followed=None
):
    if request.method == 'GET':
        data = {follow: request.user.id, followed: recipe_pk}
        serializer = acted_serializer(data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe_serializer = response_serializer(
            response_model.objects.get(id=recipe_pk),
            context={'request': request}
        )
        return Response(recipe_serializer.data)
    else:
        try:
            filter = {follow: request.user, followed + '_id': recipe_pk}
            acted_model.objects.get(**filter).delete()
        except Model.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': f'В {acted_model.__name__} связи нет'},
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUpdateRecipeMixin:

    def update(self, instance, validated_data):
        """
        update для сохранения связанных записей
        Рецепт модифицируется, только при правильности ингедиентов
        """
        ingredient_list = []
        for ingredient in validated_data.pop('ingredients'):
            ingredient_list.append({
                'recipe': self.instance.id,
                'ingredient': ingredient['ingredient']['id'],
                'amount': ingredient['ingredient']['amount'],
            })
        ingredient_serializer = RecipeIngredientsSerializer(
            data=ingredient_list,
            many=True
        )
        recipe_serializer = SimpleRecipeSerializer(
            data=validated_data,
            partial=True
        )
        valid = ingredient_serializer.is_valid() & recipe_serializer.is_valid()
        if valid:
            super().update(instance, validated_data)
            self.instance.ingredients.all().delete()
            ingredient_serializer.save()
        else:
            raise serializers.ValidationError(
                detail=(ingredient_serializer.errors, recipe_serializer.errors)
            )
        return instance

    def create(self, validated_data):
        """
        create для сохранения связанных записей
        Рецепт содается, только при правильности ингедиентов
        """
        ingredients = validated_data.pop('ingredients')
        recipe_serializer = SimpleRecipeSerializer(
            data=validated_data, partial=True
        )
        if recipe_serializer.is_valid():
            recipe_serializer.save(author=self.context['request'].user)
        else:
            raise serializers.ValidationError(detail=recipe_serializer.errors)
        recipe = recipe_serializer.instance
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append({
                'recipe': recipe.id,
                'ingredient': ingredient['ingredient']['id'],
                'amount': ingredient['ingredient']['amount'],
            })
        ingredient_serializer = RecipeIngredientsSerializer(
            data=ingredient_list, many=True
        )
        if ingredient_serializer.is_valid():
            ingredient_serializer.save()
            return recipe
        else:
            recipe.delete()
            raise serializers.ValidationError(
                detail=ingredient_serializer.errors
            )