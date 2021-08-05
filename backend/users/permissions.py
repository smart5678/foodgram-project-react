from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Разрешает полный доступ для пользователя с ролью admin
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    SAFE_METHODS для всех, полный доступ для админа
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class AdminModeratorAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Редактирование возможно только определённым пользователям
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        )

class MeNotAuthenticated(permissions.BasePermission):
    """
    Редактирование возможно только определённым пользователям
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous and view.action == 'me':
            return False
        return True
