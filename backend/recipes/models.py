from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class Tag(models.Model):
    """
    Модель тэгов рецепта
    """
    name = models.CharField('Название', max_length=200)
    color = models.CharField('Цвет в HEX', max_length=200, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.slug} - HEX {self.color}'


class Ingredient(models.Model):
    """
    Ингридиенты
    """
    name = models.CharField(
        'Название',
        unique=True,
        blank=False,
        null=False,
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200,
        blank=False
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """
    Модель recipe
    Поля модели:
    author: автор рецепта
    name: Название рецепта
    description: Описание
    ingredients: ингридиенты
    tags: тэги
    cooking_time: время приготовления
    """
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name="recipes",
        blank=True
    )
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.DurationField('Время приготовления (в минутах)')

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


### https://stackoverflow.com/questions/28706072/drf-3-creating-many-to-many-update-create-serializer-with-though-table
class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.FloatField('Количество в рецепте')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='recipe-ingredient'
        ), ]
