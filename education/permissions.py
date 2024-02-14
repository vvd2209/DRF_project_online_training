from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором."

    def has_permission(self, request, view):

        if request.user.role == UserRoles.MODERATOR:
            return True

        return False


class IsOwner(BasePermission):
    message = "Вы не являетесь владельцем"

    def has_permission(self, request, obj):

        if request.user.role == obj.owner:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
