from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredients, Tag


@admin.register(RecipeIngredients)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient')
    fields = (('recipe',), ('ingredient', 'amount'))
    list_editable = ('ingredient', 'amount', )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Ingredient в Админ.панели
    """
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    fields = (('name', 'measurement_unit'),)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Tag в Админ.панели
    """
    list_display = ('pk', 'name', 'slug', 'color')
    list_editable = ('slug', 'color')
    empty_value_display = '-пусто-'


class IngredientInline(admin.TabularInline):
    """
    Инлайн редактирование игредиентов в рецепте
    """
    model = RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Recipe в Админ.панели
    """
    fields = (
        ('name', 'author'),
        'tags',
        'image',
        'cooking_time',
        'text',
    )
    list_display = ('pk', 'name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = [IngredientInline]
    empty_value_display = '-пусто-'
