from rest_framework import permissions


class MeNotAuthenticated(permissions.BasePermission):
    """
    Редактирование возможно только определённым пользователям
    """
    def has_permission(self, request, view):
        return request.user.is_anonymous and view.action == 'me'
