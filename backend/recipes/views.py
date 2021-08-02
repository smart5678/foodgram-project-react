from django.db.models import Case, When, Value
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from backend.paginator import ResultsSetPagination
from social.models import Favorite
from social.serializers import FavoriteSerializer, FavoriteRecipeSerializer
from .models import Recipe, Tag, Ingredient
from .serializers import (RecipeSerializer, TagSerializer, IngredientSerializer)

USER = get_user_model()


class RecipeFilterBackend(BaseFilterBackend):
    """
    Бэкэнд для филтрации тэгов
    """
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.getlist('tags')
        is_favorited = request.query_params.get('is_favorited')
        if is_favorited and is_favorited == 'true':
            favorited = queryset.filter(favorited__user=request.user)
        else:
            favorited = queryset
        if tags:
            tagged = favorited.filter(tags__slug__in=tags).distinct()
        else:
            tagged = favorited

        return tagged


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с рецептами
    Фильтруется по автору или по тэгам (TagsFilterBackend)
    Паджинация берется из параметра limit запросе
    """
    model = Recipe
    serializer_class = RecipeSerializer
    pagination_class = ResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all().order_by('-pk')
    filter_backends = [DjangoFilterBackend, RecipeFilterBackend]
    filterset_fields = ['author', ]

    @action(methods=['get', 'delete'], detail=True, permission_classes=[IsAuthenticatedOrReadOnly],
            url_path='favorite', url_name='favorite')
    def set_favorite(self, request, pk=None):
        if request.method == 'GET':
            Favorite.objects.create(user=request.user, favorite_recipe_id=pk)
            serializer = FavoriteRecipeSerializer(Recipe.objects.get(id=pk), context={'request': request})
            return Response(serializer.data)
        else:
            Favorite.objects.get(user=request.user, favorite_recipe_id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с тэгами
    """
    model = Tag
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet с фильтром по ингредиентам.
    Фильтрует по вхождению в поле name параметра запроса name
    Возвращает сначала совпадающие с началом строки
    """
    model = Ingredient
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            queryset = Ingredient.objects.filter(name__contains=name)
            return queryset.annotate(
                is_start=Case(
                    When(name__startswith=name, then=Value(1)),
                    default=Value(2)
                    ),
                ).order_by('is_start')

        return Ingredient.objects.all()
