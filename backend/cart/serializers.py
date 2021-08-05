from cart.models import Cart
from rest_framework import serializers


class CartRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('recipe', 'user'),
                message="Рецепт уже добавлен в корзину"
            )
        ]
