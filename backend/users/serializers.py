from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя на основе модели
    """

    class Meta:
        model = USER
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed'
        )

