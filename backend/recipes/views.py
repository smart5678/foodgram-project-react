from django.db.models import Case, When, Value
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Recipe, Tag, Ingredient
from .serializers import (RecipeSerializer, TagSerializer, IngredientSerializer)

USER = get_user_model()


class RecipeFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.getlist('tags')
        filtered_queryset = queryset
        if tags:
            filtered_queryset = filtered_queryset.filter(tags__slug__in=tags).distinct()
        return filtered_queryset


class RecipeResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями
    """
    model = Recipe
    serializer_class = RecipeSerializer
    pagination_class = RecipeResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all().order_by('-pk')
    filter_backends = [DjangoFilterBackend, RecipeFilterBackend]
    filterset_fields = ['author', ]


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с тэгами
    """
    model = Tag
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
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
