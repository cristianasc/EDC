from rest_framework import permissions
from .exceptions import Forbidden


class MustBeSuperUser(permissions.BasePermission):
    def __init__(self, message, user=None):
        if user is not None and user.is_superuser is False:
            raise Forbidden(message)
        else:
            self.message = message

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser is True


class UserIsUser:
    def __init__(self, user, instance, message):
        if instance != user:
            raise Forbidden(message)


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.is_superuser
        return False


class IsAccountOwner(permissions.BasePermission):
    """
    Verify if user is the Account Owner - to avoid other users to change data from others
    """

    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user

        return False