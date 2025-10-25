from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Пользовательское разрешение для проверки, является ли текущий пользователь владельцем объекта.
    Используется для ограничения доступа к объекту только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяет права пользователя на доступ к объекту"""

        return obj.user == request.user
