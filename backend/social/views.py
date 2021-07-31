from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from backend.paginator import ResultsSetPagination
from users.serializers import UserSerializer

USER = get_user_model()


class SubscriptionsViewSet(viewsets.ModelViewSet):
    model = USER
    serializer_class = UserSerializer()
    permission_classes = [IsAuthenticated]
    pagination_class = ResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        print(self.request.user)
        return USER.objects.filer(subscribed=self.request.user)
