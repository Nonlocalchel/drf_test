from http import HTTPMethod

from rest_framework import permissions

from users.permissions import *


class WorkerTasksAccessPermission(IsWorker):
    def has_permission(self, request, view):
        has_base_perm = super().has_permission(request, view)
        if not has_base_perm:
            return False

        worker_ids_in_params = request.GET.get('worker')
        if worker_ids_in_params is not None:
            worker_ids = worker_ids_in_params.split(',')
            for worker_id in worker_ids:
                if worker_id not in [str(request.user.id), 'null']:
                    return False

            return True


class CustomerTasksAccessPermission(IsCustomer):
    def has_permission(self, request, view):
        has_base_perm = super().has_permission(request, view)
        if not has_base_perm:
            return False

        customer_id_in_params = request.GET.get('customer')
        if customer_id_in_params is not None:
            customer_id = customer_id_in_params[0]
            if customer_id == request.user.id:
                return True


class IsWorkerOrNobodyTask(IsWorker):
    def has_object_permission(self, request, view, obj):
        has_base_perm = super().has_permission(request, view)
        if not has_base_perm:
            return False

        if obj.worker is not None:
            return obj.worker == request.user.worker

        return True


class PatchThatIfIsWorkerOrNobodyTask(IsWorkerOrNobodyTask):
    def has_object_permission(self, request, view, obj):
        has_base_perm = super().has_permission(request, view)
        if not has_base_perm:
            return False

        if request.method == HTTPMethod.PATCH:
            return True


class IsCustomerTask(IsCustomer):
    def has_object_permission(self, request, view, obj):
        has_base_perm = super().has_permission(request, view)
        if not has_base_perm:
            return False

        if obj.customer is not None:
            return obj.customer == request.user.customer


class IsRunningTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.status == 'in_process'
