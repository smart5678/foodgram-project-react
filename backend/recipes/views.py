import io

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from cart.models import Cart
from cart.serializers import CartRecipeSerializer
from cart.temprecipe import get_invoice
from recipes.paginator import ResultsSetPagination
from social.models import Favorite
from social.serializers import FavoriteRecipeSerializer, SimpleRecipeSerializer

from .backends import IngredientFilterBackend, RecipeFilterBackend
from .mixins import set_action
from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer

USER = get_user_model()


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
    queryset = Recipe.objects.prefetch_related(
        'ingredients__ingredient'
    ).all().order_by('-pk')
    filter_backends = [DjangoFilterBackend, RecipeFilterBackend]
    filterset_fields = ['author', ]

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[IsAuthenticated],
            url_path='favorite', url_name='favorite')
    def set_favorite(self, request, pk=None):
        return set_action(
            self, request, pk,
            acted_serializer=FavoriteRecipeSerializer,
            response_serializer=SimpleRecipeSerializer,
            acted_model=Favorite,
            response_model=Recipe,
            follow='user',
            followed='favorite_recipe'
        )

    @action(methods=['get', 'delete'], detail=True,
            permission_classes=[IsAuthenticated],
            url_path='shopping_cart', url_name='shopping_cart')
    def set_shopping_cart(self, request, pk=None):
        return set_action(
            self, request, pk,
            acted_serializer=CartRecipeSerializer,
            response_serializer=SimpleRecipeSerializer,
            acted_model=Cart,
            response_model=Recipe,
            follow='user',
            followed='recipe'
        )

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def set_download_shopping_cart(self, request):
        recipes_in_cart = Cart.objects.filter(
            user=request.user
        ).values_list('recipe__id')

        ingredients = (
            RecipeIngredient.objects.select_related('ingredient')
            .filter(recipe__id__in=recipes_in_cart)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
        )
        buffer = io.BytesIO
        get_invoice(ingredients, buffer)
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='cart.pdf')


class TagViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet тэгов
    """
    model = Tag
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


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
