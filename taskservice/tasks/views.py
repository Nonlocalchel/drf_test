from rest_framework import generics
from django.shortcuts import render

from .models import Task
from .serializer import TaskSerializer


# Create your views here.

class TaskAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
