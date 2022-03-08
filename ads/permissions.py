from rest_framework import permissions

from ads.models import User


class AdUpdateDeletePermission(permissions.BasePermission):
    message = 'Allowed only for the author or admin role'

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN or request.user.id == view.get_object().author.id


class IsOwner(permissions.BasePermission):
    message = 'Allowed only for the author'

    def has_permission(self, request, view):
        return request.user.id == view.get_object().owner.id


class IsAuthor(permissions.BasePermission):
    message = 'Allowed only for the author'

    def has_permission(self, request, view):
        return request.user.id == view.get_object().author.id


class IsAdmin(permissions.BasePermission):
    message = 'Allowed only for admins'

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN
