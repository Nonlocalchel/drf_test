from rest_framework import permissions

from tasks.messages.permission_denied import TaskPermissionMessages


class WorkerTasksAccessPermission(permissions.BasePermission):
    message = TaskPermissionMessages.WORKER_TASKS_ACCESS

    def has_permission(self, request, view):
        worker_ids_in_params = request.GET.get('worker')
        if worker_ids_in_params is not None:
            request_worker_ids = worker_ids_in_params.split(',')

            user_worker_id = str(request.user.worker.id)
            for request_worker_id in request_worker_ids:
                if request_worker_id not in [user_worker_id, 'null']:
                    return False

            return True


class CustomerTasksAccessPermission(permissions.BasePermission):
    message = TaskPermissionMessages.CUSTOMER_TASKS_ACCESS

    def has_permission(self, request, view):
        customer_id = request.GET.get('customer')
        if customer_id is not None:
            user_customer_id = str(request.user.customer.id)
            if customer_id == user_customer_id:
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


class IsNotRunningTask(permissions.BasePermission):
    message = TaskPermissionMessages.RUNNING_TASK_ACCESS

    def has_object_permission(self, request, view, obj):
        return not obj.status == 'in_process'
