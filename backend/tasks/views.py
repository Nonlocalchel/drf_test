from http import HTTPMethod

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from services.SelectPermissionByActionMixin import SelectPermissionByActionMixin
from .filters import TaskFilter
from .models import Task
from users.permissions import *
from .permissions import *
from .serializers import (
    TaskReadSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskPartialUpdateSerializer
)


# Create your views here.
class CRUViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                 mixins.ListModelMixin, mixins.UpdateModelMixin,
                 GenericViewSet):
    pass


class TaskViewSet(SelectPermissionByActionMixin, CRUViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskReadSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'status']
    permission_classes_by_action = {
        'list': [IsWorker & WorkerTasksAccessPermission | IsCustomer & CustomerTasksAccessPermission | IsSuperWorker],
        'retrieve': [IsWorker & WorkerTaskAccessPermission | IsCustomer & CustomerTaskAccessPermission | IsSuperWorker],
        'update': [IsNotRunningTask & IsCustomer & CustomerTaskAccessPermission],
        'create': [IsCustomer & CustomerTaskAccessPermission | IsSuperWorker]
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
        request.data['worker'] = request.user
        return self._partial_update_status(request.data)

    @action(detail=True, methods=[HTTPMethod.PATCH],
            permission_classes=[IsWorker & WorkerTaskAccessPermission])
    def done(self, request, pk=None):
        request.data['status'] = Task.StatusType.DONE
        return self._partial_update_status(request.data)

    def _partial_update_status(self, request_data: Request) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.check_user_type('customer'):
            request.data['customer'] = user.id

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)