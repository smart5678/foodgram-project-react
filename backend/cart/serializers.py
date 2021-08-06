from rest_framework import serializers

from cart.models import Cart


class CartRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('recipe', 'user'),
                message='Рецепт уже добавлен в корзину'
            )
        ]
