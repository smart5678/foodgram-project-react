from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from backend.paginator import ResultsSetPagination
from social.models import Follow
from social.serializers import SubscriberSerializer
from users.serializers import UserSerializer

USER = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = ResultsSetPagination
    serializer_class = UserSerializer
    queryset = USER.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticatedOrReadOnly],
            url_path='subscribe', url_name='subscribe')
    def set_subscribe(self, request, id=None):
        print('hello', id, request.user)
        Follow.objects.create(user=request.user, author_id=id)
        serializer = SubscriberSerializer(USER.objects.get(pk=id), context={'request': request})
        print(serializer.data)
        return Response(serializer.data)

    @action(methods=['delete'], detail=True, permission_classes=[IsAuthenticatedOrReadOnly],
            url_path='subscribe', url_name='subscribe')
    def set_unsubscribe(self, request, id=None):
        pass





