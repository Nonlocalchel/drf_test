from rest_framework import permissions

from users.services.utils import *


class IsWorker(permissions.BasePermission):
    message = 'You are not a worker!'

    def has_permission(self, request, view):
        user = request.user
        return user.check_user_type('worker')


class IsCustomer(permissions.BasePermission):
    message = 'You are not a customer!'

    def has_permission(self, request, view):
        user = request.user
        return user.check_user_type('customer')


class IsSuperCustomer(permissions.BasePermission):
    message = 'You are not a customer with extra permissions!'

    def has_permission(self, request, view):
        user = request.user
        if user.check_user_type('customer'):
            return is_super_customer(user)


class IsSuperWorker(permissions.BasePermission):
    message = 'You are not a worker with extra permissions!'

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
