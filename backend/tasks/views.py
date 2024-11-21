from http import HTTPMethod

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter

from services.mixins.permissions import SelectPermissionByActionMixin
from services.viewsets import CRUViewSet
from .utils import filter_task_queryset, take_task_in_process, done_task, set_task_customer
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
    """Tasks app view"""
    queryset = Task.objects.all()
    serializer_class = TaskReadSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TaskFilter
    search_fields = ['title']
    permission_classes_by_action = {
        'retrieve': [IsSuperWorker | WorkerTaskAccessPermission | CustomerTaskAccessPermission],
        'update': [IsNotRunningTask & CustomerTaskAccessPermission],
        'create': [IsSuperWorker | CustomerTaskAccessPermission]
    }

    def get_queryset(self):
        """Optimize get users queryset and filter queryset for request /tasks/ and fix swagger issues"""
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return Task.objects.none()

        queryset = self.queryset
        if self.action == 'list':
            user = self.request.user
            queryset = filter_task_queryset(user, self.queryset)

        return queryset

    def get_serializer_class(self):
        """Choose serializer by http method"""
        serializer_classes_by_method = {
            HTTPMethod.GET: TaskReadSerializer,
            HTTPMethod.POST: TaskCreateSerializer,
            HTTPMethod.PUT: TaskUpdateSerializer,
            HTTPMethod.PATCH: TaskPartialUpdateSerializer
        }

        req_method = self.request.method
        serializer_class = serializer_classes_by_method[req_method]
        return serializer_class

    def create(self, request, *args, **kwargs):
        """Set customer id if customer create task"""
        set_task_customer(request.data, request.user)
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        """Forbidden http method patch for /tasks/ url"""
        raise MethodNotAllowed(request.method)

    @action(detail=True, methods=[HTTPMethod.PATCH], permission_classes=[IsWorker])
    def take_in_process(self, request, pk):
        """Take task in process by /tasks-take-in-process/ url"""
        take_task_in_process(request.data, request.user)
        return self.update(request, partial=True)

    @action(detail=True, methods=[HTTPMethod.PATCH], permission_classes=[WorkerTaskAccessPermission])
    def done(self, request, pk):
        """Done task by /tasks-done/ url"""
        done_task(request.data)
        return self.update(request, partial=True)
