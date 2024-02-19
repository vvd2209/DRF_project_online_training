from rest_framework import permissions
from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='MODERATOR').exists()

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='MODERATOR').exists():
            return True
        return obj.owner == request.user


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelfUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email
