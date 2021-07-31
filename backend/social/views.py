from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated

from backend.paginator import ResultsSetPagination
from users.serializers import UserSerializer

USER = get_user_model()


class SubscriptionsViewSet(UserViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        return USER.objects.filter(subscribed__in=self.request.user.subscriber.all())
