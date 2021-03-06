from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from rest_framework import serializers, status
from rest_framework.response import Response

from recipes.models import Recipe, RecipeIngredient

# Заголовок таблицы скачанных ингредиентов
HEADER = ['#', 'Ингредиент', 'Кол-во', 'Ед.изм.']


class IngredientFieldSetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(IngredientFieldSetSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RecipeIngredientsSerializer(IngredientFieldSetSerializer):

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
        errors = {}
        recipe_serializer = SimpleRecipeSerializer(data=data, partial=True)
        try:
            recipe_serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as exc:
            errors = {**exc.detail}

        ingredient_errors = []
        amount_serializer = RecipeIngredientsSerializer(
            data=ingredients,
            many=True,
            fields=('amount',)
        )
        try:
            amount_serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            ingredient_errors = [error['amount'] for
                                 error in amount_serializer.errors if error]
        # validate unique ingredient before affecting the model
        ingredients_id = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_id:
                ingredient_errors.append('Ингредиенты дублируются')
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
        except acted_model.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': f'В {acted_model.__name__} связи нет'},
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_invoice(ingredients, file):
    data = [HEADER]
    for row, ingredient in enumerate(ingredients):
        data.append([
            row + 1,
            ingredient['ingredient__name'],
            ingredient['total_amount'],
            ingredient['ingredient__measurement_unit']
        ])

    doc = SimpleDocTemplate(file, pagesize=A4)
    elements = []
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    table = Table(
        data,
        [1 * cm, 12 * cm, 2 * cm, 4 * cm],
        len(data) * [1 * cm])
    table.setStyle(
        TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.02 * cm, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.035 * cm, colors.black),
                    ('FONT', (0, 0), (-1, -1), 'DejaVuSerif', 14),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
    elements.append(table)
    doc.build(elements)
