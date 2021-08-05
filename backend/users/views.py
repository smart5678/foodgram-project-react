from django.core.exceptions import ObjectDoesNotExist

from recipes.mixins import set_action
from recipes.paginator import ResultsSetPagination
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response
from social.models import Follow
from social.serializers import SubscriberSerializer, FollowSerializer
from users.permissions import MeNotAuthenticated
from users.serializers import UserSerializer

USER = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = ResultsSetPagination
    serializer_class = UserSerializer
    queryset = USER.objects.all()
    permission_classes = [MeNotAuthenticated, IsAuthenticatedOrReadOnly]

    @action(methods=['get', 'delete'], detail=True, permission_classes=[IsAuthenticatedOrReadOnly],
            url_path='subscribe', url_name='subscribe')
    def set_subscribe(self, request, id=None):
        return set_action(
            self, request, id,
            acted_serializer=FollowSerializer,
            ressponse_serializer=SubscriberSerializer,
            acted_model=Follow,
            response_model=USER,
            follow='user',
            followed='author'
        )

