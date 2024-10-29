from rest_framework import permissions

from .messages.permission_denied import UserPermissionMessages
from .models import User


class IsWorker(permissions.BasePermission):
    """Checks that the user is a worker"""
    message = UserPermissionMessages.WORKER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False

        return user.check_user_type(User.UserType.WORKER)


class IsCustomer(permissions.BasePermission):
    """Checks that the user is a customer"""
    message = UserPermissionMessages.CUSTOMER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False

        return user.check_user_type(User.UserType.CUSTOMER)


class IsSuperCustomer(permissions.BasePermission):
    """Checks that the user is a customer with extra permissions"""
    message = UserPermissionMessages.SUPER_CUSTOMER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        user_is_customer = super().has_permission(request, view)
        if not user_is_customer:
            return False

        return user.is_staff


class IsSuperWorker(IsWorker):
    """Checks that the user is a worker with extra permissions"""
    message = UserPermissionMessages.SUPER_WORKER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        user_is_worker = super().has_permission(request, view)
        if not user_is_worker:
            return False

        return user.is_staff


class IsUserAccount(permissions.BasePermission):
    """Checks that is object is a user account"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_anonymous:
            return False

        return obj == user