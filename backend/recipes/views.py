from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from users.permissions import (AdminModeratorAuthorOrReadOnly,
                                  IsAdminOrReadOnly)

from .models import Recipe, Tag, Ingredient
from .serializers import (RecipeSerializer, TagSerializer, IngredientSerializer)

USER = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями
    """
    model = Recipe
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с тэгами
    """
    model = Tag
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
    model = Ingredient
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
