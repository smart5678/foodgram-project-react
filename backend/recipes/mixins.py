from django.db.models import Model
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from recipes.models import Recipe, RecipeIngredient


class RecipeIngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """
    Используется для спсиков избранного и корзины
    С его помощью валидируются несвязанные поля.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
            'author',
            'text',
            'tags'
        )


class CreateUpdateMixin:
    """
    Миксины для модели рецептов Реализует методы update(), create()
    Валидирует поля модели без учета поля ингредиента.
    Ингредиент валидируется в методах update(), create(),
    т.к. вложеной модели нужен инстанс рецепта.
    """

    def validate(self, data):
        ingredients = data.pop('ingredients')
        ingredients_id = []
        errors = {}
        recipe_serializer = SimpleRecipeSerializer(data=data, partial=True)
        try:
            recipe_serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            errors = {**exc.detail}
        ingredient_errors = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_id:
                ingredient_errors.append(
                    {'ingredient': ['Ингредиенты дублируются']}
                )
            if (not isinstance(ingredient['amount'], int)
                    or ingredient['amount'] < 0):
                ingredient_errors.append(
                    {'ingredient': ['Введите правльное число']}
                )
            ingredients_id.append(ingredient['id'])
        if ingredient_errors:
            errors['ingredients'] = ingredient_errors
        if errors:
            raise serializers.ValidationError(errors)
        validated_data = recipe_serializer.validated_data
        validated_data['ingredients'] = ingredients
        return validated_data

    def update(self, instance, validated_data):
        """
        update для сохранения связанных записей
        Рецепт модифицируется, только при правильности ингедиентов
        Влидируем ингредиенты. даляем старые, сохраняем новые,
        обновляем основные поля модели рецепта
        """
        ingredients = []
        for ingredient in validated_data.pop('ingredients'):
            ingredients.append({
                'recipe': self.instance.id or None,
                'ingredient': ingredient['id'],
                'amount': ingredient['amount'],
            })
        ingredient_serializer = RecipeIngredientsSerializer(
            data=ingredients,
            many=True,
        )
        ingredient_serializer.is_valid(raise_exception=True)
        self.instance.ingredients.all().delete()
        ingredient_serializer.save()
        super().update(instance, validated_data)
        return instance

    def create(self, validated_data):
        """
        create для сохранения связанных записей
        Рецепт содается, только при правильности ингедиентов
        """
        ingredients = validated_data.pop('ingredients')
        recipe_serializer = SimpleRecipeSerializer(
            data=validated_data,
            partial=True
        )
        validated_data['author'] = self.context['request'].user
        recipe = recipe_serializer.create(validated_data)

        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append({
                'recipe': recipe.id,
                'ingredient': ingredient['id'],
                'amount': ingredient['amount'],
            })
        ingredient_serializer = RecipeIngredientsSerializer(
            data=ingredient_list,
            many=True,
        )
        if not ingredient_serializer.is_valid():
            recipe.delete()
            raise serializers.ValidationError(ingredient_serializer.errors)
        ingredient_serializer.save()
        return recipe


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
