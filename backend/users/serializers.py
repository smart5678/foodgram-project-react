from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import SerializerMethodField

USER = get_user_model()


class UserSerializer(UserSerializer):
    """
    Сериализатор пользователя
    """
    is_subscribed = SerializerMethodField()

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

    def get_is_subscribed(self, author):
        """
        false for not authentificated and self
        """
        user = self.context['request'].user
        return (user.is_authenticated
                and user.subscriber.filter(author=author).exists())
