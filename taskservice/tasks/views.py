from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Task
from .permissions import IsTaskInvolvedPerson
from .serializers import *


# Create your views here.
class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                  GenericViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.type == 'customer':
            return self.queryset.filter(customer=user.id)

        if user.type == 'worker':
            return self.queryset.filter(worker=user.id)

        return super().get_queryset()

    #метод для получения всех записей по отд. адресу

    def get_serializer_class(self):
        if self.request.method == "POST":
            user = self.request.user
            if user.type == 'customer':
                return CustomerTaskCreateSerializer

            if user.type == 'worker':
                return WorkerTaskCreateSerializer

        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def all(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


    # def get_permissions(self):
    #     if self.action == 'update':

    # @action(methods=['put'], detail=True,
    #         url_path='close-task', url_name='close-task')
    # def close_task(self, request, pk=None):