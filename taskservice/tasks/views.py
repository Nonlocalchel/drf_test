from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.filters import SearchFilter
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
    filter_backends = [DjangoFilterBackend, SearchFilter] #
    filterset_class = TaskFilter
    search_fields = ['title','status']
    permission_classes_by_action = {
        'list': [IsWorker & WorkerTasksAccessPermission | IsCustomer & CustomerTasksAccessPermission | IsSuperWorker],
        'retrieve': [IsWorker & WorkerTaskAccessPermission | IsCustomer & CustomerTaskAccessPermission | IsSuperWorker],
        'partial_update': [IsWorker & WorkerTaskAccessPermission],
        'update': [IsNotRunningTask & IsCustomer & CustomerTaskAccessPermission],
        'create': [IsCustomer & CustomerTaskAccessPermission | IsSuperWorker]
    }

    def get_serializer_class(self):
        serializer_classes_by_method = {
            'get': TaskReadSerializer,
            'post': TaskCreateSerializer,
            'put': TaskUpdateSerializer,
            'patch': TaskPartialUpdateSerializer
        }

        req_method = self.request.method.lower()
        serializer_class = serializer_classes_by_method[req_method]
        return serializer_class

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.check_user_type('customer'):
            request.data['customer'] = user.id

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        request.data['worker'] = request.user

        return super().partial_update(request, *args, **kwargs)

