from http import HTTPMethod

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter

from services.mixins.permissions import SelectPermissionByActionMixin
from services.viewsets import CRUViewSet
from .filters import TaskFilter
from users.permissions import *
from .permissions import *
from .serializers import (
    TaskReadSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskPartialUpdateSerializer
)


# Create your views here.


class TaskViewSet(SelectPermissionByActionMixin, CRUViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskReadSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'status']
    permission_classes_by_action = {
        'list': [IsSuperWorker | WorkerTasksAccessPermission | CustomerTasksAccessPermission],
        'retrieve': [IsSuperWorker | WorkerTaskAccessPermission | CustomerTaskAccessPermission],
        'update': [IsNotRunningTask & CustomerTaskAccessPermission],
        'create': [IsSuperWorker | CustomerTaskAccessPermission]
    }

    def get_serializer_class(self):
        serializer_classes_by_method = {
            HTTPMethod.GET: TaskReadSerializer,
            HTTPMethod.POST: TaskCreateSerializer,
            HTTPMethod.PUT: TaskUpdateSerializer,
            HTTPMethod.PATCH: TaskPartialUpdateSerializer
        }

        req_method = self.request.method
        serializer_class = serializer_classes_by_method[req_method]
        return serializer_class

    @action(detail=True, methods=[HTTPMethod.PATCH],
            permission_classes=[IsWorker & WorkerTaskAccessPermission])
    def take_in_process(self, request, pk=None):
        request.data['worker'] = request.user.worker.id
        return self.update(request, partial=True)

    @action(detail=True, methods=[HTTPMethod.PATCH],
            permission_classes=[IsWorker & WorkerTaskAccessPermission])
    def done(self, request, pk=None):
        request.data['status'] = Task.StatusType.DONE
        return self.update(request, partial=True)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.check_user_type('customer'):
            request.data['customer'] = user.customer.id

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
