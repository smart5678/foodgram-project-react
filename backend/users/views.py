from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

from users.serializers import UserSerializer

USER = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    model = USER
    serializer_class = UserSerializer()
    queryset = USER.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]


class SubscriptionsViewSet(viewsets.ModelViewSet):
    model = USER
    serializer_class = UserSerializer()
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return USER.objects.filer(subscriber=self.request.user)