from rest_framework import permissions


class IsTaskInvolvedPerson(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.id == obj.customer:
            return True

        if user.id == obj.worker:
            return True

        if hasattr(user, 'worker'):
            return user.worker.is_super_worker


class IsWorkerAndTaskIsFree(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.type == 'worker' and not obj.worker
