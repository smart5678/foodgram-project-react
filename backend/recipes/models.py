from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, \
    integer_validator
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


class Recipe(models.Model):
    """
    Модель recipe
    Поля модели:
    author: автор рецепта
    name: Название рецепта
    description: Описание
    ingredients: ингредиенты
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
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1, 'Быстрее не получится'),
            integer_validator
        ]
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ингредиенты
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
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество в рецепте',
        validators=[
            MinValueValidator(1, message='Добавьте количество'),
            integer_validator
        ]
    )

    class Meta:
        # constraints = [models.UniqueConstraint(
        #     fields=['recipe', 'ingredient'],
        #     name='recipe-ingredients'
        # ), ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
