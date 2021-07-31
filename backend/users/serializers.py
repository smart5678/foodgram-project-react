from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя на основе модели
    """
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, author):
        """
        false for not authentificated and self
        """
        user = self.context['request'].user
        if user.is_authenticated and user.subscriber.filter(author=author):
            return True
        return False

    class Meta:
        model = USER
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

