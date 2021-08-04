from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.paginator import ResultsSetPagination
from social.serializers import SubscriberSerializer

USER = get_user_model()


class SubscriptionsViewSet(UserViewSet):

    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        return USER.objects.filter(subscribed__user=self.request.user)

