from rest_framework import permissions

from tasks.messages.permission_denied import TaskPermissionMessages


class WorkerTasksAccessPermission(permissions.BasePermission):
    message = TaskPermissionMessages.WORKER_TASKS_ACCESS

    def has_permission(self, request, view):
        worker_ids_in_params = request.GET.get('worker')
        if worker_ids_in_params is not None:
            worker_ids = worker_ids_in_params.split(',')
            for worker_id in worker_ids:
                if worker_id not in [str(request.user.id), 'null']:
                    return False

            return True


class CustomerTasksAccessPermission(permissions.BasePermission):
    message = TaskPermissionMessages.CUSTOMER_TASKS_ACCESS

    def has_permission(self, request, view):
        customer_id_in_params = request.GET.get('customer')
        if customer_id_in_params is not None:
            customer_id = customer_id_in_params[0]
            if customer_id == request.user.id:
                return True


class WorkerTaskAccessPermission(permissions.BasePermission):
    message = TaskPermissionMessages.WORKER_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        if obj.worker is not None:
            return obj.worker == request.user.worker

        return True


class CustomerTaskAccessPermission(permissions.BasePermission):
    message = TaskPermissionMessages.CUSTOMER_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.customer


class IsRunningTask(permissions.BasePermission):
    message = TaskPermissionMessages.RUNNING_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        return obj.status == 'in_process'
