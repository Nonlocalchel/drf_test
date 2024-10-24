from rest_framework import permissions

from tasks.messages.permission_denied import TaskPermissionMessages
from users.permissions import IsWorker, IsCustomer
from .models import Task


class IsNotRunningTask(permissions.BasePermission):
    message = TaskPermissionMessages.RUNNING_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        return obj.status == Task.StatusType.WAIT


class IsProcessedTask(permissions.BasePermission):
    message = TaskPermissionMessages.RUNNING_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        return obj.status == Task.StatusType.IN_PROCESS
