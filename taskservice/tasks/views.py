from rest_framework import mixins
from rest_framework.decorators import action
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

        return super().get_queryset()
    # def get_serializer_class(self):
    #     if self.request.method in ['PUT', 'PATCH']:

    # def get_permissions(self):
    #     if self.action == 'update':

    # @action(methods=['put'], detail=True,
    #         url_path='close-task', url_name='close-task')
    # def close_task(self, request, pk=None):