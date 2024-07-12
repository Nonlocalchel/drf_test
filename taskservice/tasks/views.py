from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Task
from .permissions import IsTaskInvolvedPerson
from .serializer import TaskSerializer, TaskUpdateSerializer


# Create your views here.
class TaskViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsTaskInvolvedPerson)

    def get_serializer_class(self):
        if self.action == 'update':
            return TaskUpdateSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action == 'update':
            return [permission() for permission in (IsWorkerAndTaskIsFree)]

        return [permission() for permission in self.permission_classes]