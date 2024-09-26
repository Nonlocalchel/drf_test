from rest_framework import permissions

from .messages.permission_denied import UserPermissionMessages
from users.utils import *


class IsWorker(permissions.BasePermission):
    message = UserPermissionMessages.WORKER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False

        return user.check_user_type('worker')


class IsCustomer(permissions.BasePermission):
    message = UserPermissionMessages.CUSTOMER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False

        return user.check_user_type('customer')


class IsSuperCustomer(permissions.BasePermission):
    message = UserPermissionMessages.SUPER_CUSTOMER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        user_is_customer = super().has_permission(request, view)
        if not user_is_customer:
            return False

        if user.check_user_type('customer'):
            return is_super_customer(user)


class IsSuperWorker(IsWorker):
    message = UserPermissionMessages.SUPER_WORKER_ACCESS

    def has_permission(self, request, view):
        user = request.user
        user_is_worker = super().has_permission(request, view)
        if not user_is_worker:
            return False

        if user.check_user_type('worker'):
            return is_super_worker(user)


class IsSuperWorkerOrReadOnly(IsSuperWorker):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super().has_permission(request, view)
