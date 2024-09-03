from rest_framework import permissions
from users.services.utils import check_user_type


class IsRunningTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.status != 'wait':
            return check_user_type(user, 'worker')
