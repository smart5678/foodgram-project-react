from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly

from backend.paginator import ResultsSetPagination
from social.serializers import SubscriberSerializer
from users.serializers import UserSerializer

USER = get_user_model()


class SubscriptionsViewSet(UserViewSet):

    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        return USER.objects.filter(subscribed__in=self.request.user.subscriber.all())

