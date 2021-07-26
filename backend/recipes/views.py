from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from users.permissions import (AdminModeratorAuthorOrReadOnly,
                                  IsAdminOrReadOnly)

from .models import Recipe
from .serializers import (RecipeSerializer, )

USER = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями
    """
    model = Recipe
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]