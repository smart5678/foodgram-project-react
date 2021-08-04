from collections import namedtuple

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, When, Value, Sum
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response

from backend.paginator import ResultsSetPagination
from cart.models import Cart
from cart.serializers import CartRecipeSerializer
from social.models import Favorite
from social.serializers import FavoriteRecipeSerializer, SimpleRecipeSerializer
from .models import Recipe, Tag, Ingredient, RecipeIngredients
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer

USER = get_user_model()


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
        if is_in_shopping_cart and is_in_shopping_cart:
            filter['purchased__user'] = request.user
        return queryset.filter(**filter).distinct()


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
    queryset = Recipe.objects.prefetch_related('ingredients__ingredient').all().order_by('-pk')
    filter_backends = [DjangoFilterBackend, RecipeFilterBackend]
    filterset_fields = ['author', ]

    @action(methods=['get', 'delete'], detail=True, permission_classes=[IsAuthenticated],
            url_path='favorite', url_name='favorite')
    def set_favorite(self, request, pk=None):
        if request.method == 'GET':
            data = {'user': request.user.id, 'favorite_recipe': pk}
            serializer = FavoriteRecipeSerializer(data=data, partial=False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                recipe_serializer = SimpleRecipeSerializer(Recipe.objects.get(id=pk), context={'request': request})
                return Response(recipe_serializer.data)
            else:
                raise serializers.ValidationError(
                    {'error': serializer.errors}
                )
        else:
            try:
                Favorite.objects.get(user=request.user, favorite_recipe_id=pk).delete()
            except ObjectDoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'В избранном рецепта нет'},
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', 'delete'], detail=True, permission_classes=[IsAuthenticated],
            url_path='shopping_cart', url_name='shopping_cart')
    def set_shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = CartRecipeSerializer(data=data, partial=False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cart_serializer = SimpleRecipeSerializer(Recipe.objects.get(id=pk), context={'request': request})
                return Response(cart_serializer.data)
            else:
                raise serializers.ValidationError(
                    {'error': serializer.errors}
                )
        else:
            try:
                Cart.objects.get(user=request.user, recipe_id=pk).delete()
            except ObjectDoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'В корзине рецепта нет'},
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated],
            url_path='download_shopping_cart', url_name='download_shopping_cart')
    def set_download_shopping_cart(self, request):
        recipes_in_cart = Cart.objects.filter(user=request.user).values_list('recipe__id')
        ingredients =\
            RecipeIngredients.objects.select_related('ingredient').\
            filter(recipe__id__in=recipes_in_cart).\
            values('ingredient__name', 'ingredient__measurement_unit').annotate(total_amount=Sum('amount'))

        return Response(ingredients)


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
    queryset = Ingredient.objects.all()
    filter_backends = [IngredientFilterBackend, ]

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


