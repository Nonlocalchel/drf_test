from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Task
from .permissions import IsTaskInvolvedPerson
from .serializers import *


# Create your views here.
class TaskViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    #permission_classes = (IsAuthenticated, IsTaskInvolvedPerson)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaskReportUpdateSerializer

        return self.serializer_class

    # def get_permissions(self):
    #     if self.action == 'update':
    #         return [permission() for permission in (IsWorkerAndTaskIsFree)]
    #
    #     return [permission() for permission in self.permission_classes]

    @action(methods=['put'], detail=True,
            url_path='close-task', url_name='close-task')
    def close_task(self, request, pk=None):
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Task.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        if instance.status != 'worker':
            return

        serializer = TaskCloseSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)