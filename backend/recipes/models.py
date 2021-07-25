from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class Tag(models.Model):
    """
    Модель тэгов рецепта
    """
    hex_code = models.CharField('Цветовой HEX-код', max_length=7)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.slug} - HEX {self.hex_code}'


class Ingredient(models.Model):
    """
    Ингридиенты
    """
    name = models.CharField(
        'Название',
        unique=True,
        blank=False,
        null=False,
        max_length=50
    )
    unit = models.CharField('Единицы измерения', max_length=10, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.unit}'


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
        Tag, verbose_name='Тэги', related_name="recipes", blank=True
    )
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    cooking_time = models.DurationField('Время приготовления')

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        related_name='ingredient',
        verbose_name='Ингридиент',
        null=True,
    )
    quantity = models.FloatField('Количество')

    class Meta:
        ordering = ['recipe']
        verbose_name = f'Ингридиент для рецепта'
        verbose_name_plural = f'Ингридиенты для рецепта'
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='recipe-ingredient'
        ), ]

    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'
