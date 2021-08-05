from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

USER = get_user_model()


class UserSerializer(UserSerializer):
    """
    Сериализатор пользователя
    """
    is_subscribed = SerializerMethodField()

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
