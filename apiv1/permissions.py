from rest_framework import permissions


class IsModelAdminPermission(permissions.BasePermission):
    """
    Только администраторы на все методы.
    """
    message = 'Только администраторы имеют доступ.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsSafeOrAdminPermission(permissions.BasePermission):
    """
    GET для всех иначе только администраторы.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAuthorOrAbovePermission(permissions.BasePermission):
    """
    POST и 'SAFE' для всех, иначе только автор, модераторы и админы.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method not in ('PUT', 'PATCH', "DELETE")
                or request.user == obj.author
                or (request.user.is_authenticated
                    and request.user.is_moderator))
