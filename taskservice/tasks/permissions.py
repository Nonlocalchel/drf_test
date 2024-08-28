from rest_framework import permissions
from .services.utils import check_user_type


class IsWorker(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return check_user_type(user, 'worker')


class IsSuperWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.worker.is_super_worker


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_user_type(user, 'customer')


class IsRunningTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.status != 'wait':
            return check_user_type(user, 'worker')
