from rest_framework import permissions

from services.exception_class_decorator import raise_permission_denied_if_false
from .messages.permission_denied import UserPermissionMessages
from .services.utils import *


class IsWorker(permissions.BasePermission):
    message = UserPermissionMessages.WORKER_ACCESS

    @raise_permission_denied_if_false(message)
    def has_permission(self, request, view):
        user = request.user
        return user.check_user_type('worker')


class IsCustomer(permissions.BasePermission):
    message = UserPermissionMessages.CUSTOMER_ACCESS

    @raise_permission_denied_if_false(message)
    def has_permission(self, request, view):
        user = request.user
        return user.check_user_type('customer')


class IsSuperCustomer(permissions.BasePermission):
    message = UserPermissionMessages.SUPER_CUSTOMER_ACCESS

    @raise_permission_denied_if_false(message)
    def has_permission(self, request, view):
        user = request.user
        if user.check_user_type('customer'):
            return is_super_customer(user)


class IsSuperWorker(permissions.BasePermission):
    message = UserPermissionMessages.SUPER_WORKER_ACCESS

    @raise_permission_denied_if_false(message)
    def has_permission(self, request, view):
        user = request.user
        if user.check_user_type('worker'):
            return is_super_worker(user)


class IsSuperWorkerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user.check_user_type('worker'):
            return is_super_worker(user)
