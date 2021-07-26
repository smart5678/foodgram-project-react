from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdminUser
from .serializers import UserSerializer

USER = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями
    """
    serializer_class = UserSerializer
    queryset = USER.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdminUser]

    # @action(detail=False, permission_classes=[IsAuthenticated],
    #         methods=['get', 'patch'])
    # def me(self, request):
    #     user = self.request.user
    #     if request.method == 'GET':
    #         serializer = self.get_serializer(user)
    #         return Response(serializer.data)
    #
    #     serializer = UserSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)