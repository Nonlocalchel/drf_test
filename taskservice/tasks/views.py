from rest_framework import generics, viewsets, mixins
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet

from .models import Task
from .serializer import TaskSerializer, TaskUpdateSerializer


# Create your views here.
class TaskViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return TaskUpdateSerializer

        return self.serializer_class
