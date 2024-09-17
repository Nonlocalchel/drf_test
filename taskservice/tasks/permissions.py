from rest_framework import permissions


class IsRunningTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.status != 'wait':
            return user.check_user_type('worker')
