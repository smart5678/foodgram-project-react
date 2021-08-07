import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.serializers import UserSerializer

from .mixins import CreateUpdateMixin
from .models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source='ingredient.pk')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(CreateUpdateMixin, serializers.ModelSerializer):
    """
    В update и create дополнительно обновляются связанные модели ингредиентов.
    """
    author = UserSerializer()
    tags = TagSerializer(many=True, read_only=True, partial=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        partial=False
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'text', 'cooking_time',
            'ingredients', 'image', 'is_favorited', 'is_in_shopping_cart'
        )

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.favorites.filter(favorite_recipe=recipe).exists())

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.buyer.filter(recipe=recipe).exists())

    def to_internal_value(self, data):
        """
        Декодирует картинку из base64, отдает путь в image модели.
        """
        internal_data = data
        if self.context.get('request').method in ['PUT', 'POST']:
            image = internal_data.pop('image')
            format, imgstr = image.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            image_file = ContentFile(
                base64.b64decode(imgstr),
                name='temp.' + ext
            )
            internal_data['image'] = image_file

        return internal_data
