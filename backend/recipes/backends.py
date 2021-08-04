from django.db.models import Case, When, Value
from rest_framework.filters import BaseFilterBackend


class IngredientFilterBackend(BaseFilterBackend):
    """
    Бэкэнд для фильтрации ингредиентов
    С сортировкой по вхождению подстроки в начало затем по алфавиту
    """
    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)
            return queryset.annotate(
                is_start=Case(
                    When(name__startswith=name, then=Value(1)),
                    default=Value(2)
                    ),
                ).order_by('is_start')
        return queryset


class RecipeFilterBackend(BaseFilterBackend):
    """
    Бэкэнд для филтрации тэгов
    """
    def filter_queryset(self, request, queryset, view):
        filter = {}
        tags = request.query_params.getlist('tags')
        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        if is_favorited and is_favorited == 'true':
            filter['favorited__user'] = request.user
        if tags:
            filter['tags__slug__in'] = tags
        if is_in_shopping_cart and is_in_shopping_cart == 'true':
            filter['purchased__user'] = request.user
        return queryset.filter(**filter).distinct()
