from django.contrib import admin
from .models import Ingredient, Tag, RecipeIngredients, Recipe


@admin.register(RecipeIngredients)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient')
    fields = (('ingredient', 'amount'),)
    list_editable = ('ingredient', 'amount', )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Ingredient в Админ.панели
    """
    list_display = ('pk', 'name', 'measurement_unit')
    fields = (('name', 'measurement_unit'),)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Tag в Админ.панели
    """
    list_display = ('slug', 'hex_code')
    empty_value_display = '-пусто-'


class IngredientInline(admin.TabularInline):
    model = RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Recipe в Админ.панели
    """
    fields = (
        ('name', 'author'),
        'tags',
        'cooking_time',
        'description',

    )
    list_display = ('name', 'author')
    inlines = [IngredientInline]
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
