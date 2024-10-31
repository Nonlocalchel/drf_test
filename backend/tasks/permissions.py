from rest_framework import permissions

from tasks.messages.permission_denied import TaskPermissionMessages
from users.permissions import IsWorker, IsCustomer
from .models import Task


class WorkerTaskAccessPermission(IsWorker):
    message = TaskPermissionMessages.WORKER_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        user_is_worker = super().has_permission(request, view)
        if not user_is_worker:
            return False

        if obj.worker_id is not None:
            return obj.worker_id == request.user.worker.id

        return True


class CustomerTaskAccessPermission(IsCustomer):
    message = TaskPermissionMessages.CUSTOMER_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        user_is_customer = super().has_permission(request, view)
        if not user_is_customer:
            return False

        return obj.customer_id == request.user.customer.id


class IsNotRunningTask(permissions.BasePermission):
    message = TaskPermissionMessages.RUNNING_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        return obj.status == Task.StatusType.WAIT
