from rest_framework import permissions

from users.services.utils import *


class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_user_type(user, 'worker')


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return check_user_type(user, 'customer')


class IsSuperCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if check_user_type(user, 'customer'):
            return is_super_customer(user)


class IsSuperWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if check_user_type(user, 'worker'):
            return is_super_worker(user)


class IsSuperWorkerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if check_user_type(user, 'worker'):
            return is_super_worker(user)
