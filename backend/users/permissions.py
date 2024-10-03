from rest_framework import permissions

from .messages.permission_denied import UserPermissionMessages
from .models import User


class IsWorker(permissions.BasePermission):
    message = UserPermissionMessages.WORKER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False

        return user.check_user_type(User.UserType.WORKER)


class IsCustomer(permissions.BasePermission):
    message = UserPermissionMessages.CUSTOMER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False

        return user.check_user_type(User.UserType.CUSTOMER)


class IsSuperCustomer(permissions.BasePermission):
    message = UserPermissionMessages.SUPER_CUSTOMER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        user_is_customer = super().has_permission(request, view)
        if not user_is_customer:
            return False

        return user.is_staff


class IsSuperWorker(IsWorker):
    message = UserPermissionMessages.SUPER_WORKER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        user_is_worker = super().has_permission(request, view)
        if not user_is_worker:
            return False

        return user.is_staff


class IsUserAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_anonymous:
            return False

        return obj == user


class IsSuperCustomerReadWorkers(IsSuperCustomer):
    def has_permission(self, request, view):
        user_is_super_customer = super().has_permission(request, view)
        if not user_is_super_customer:
            return False

        users_query_type = request.GET.get('type')
        return users_query_type == User.UserType.WORKER
