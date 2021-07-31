from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from backend.paginator import ResultsSetPagination
from users.serializers import UserSerializer

USER = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = ResultsSetPagination
    serializer_class = UserSerializer
    queryset = USER.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]










