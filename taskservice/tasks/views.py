from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS

from .models import Task
from .permissions import *
from .serializers import JobSerializer, JobCreateSerializer, TaskSerializer

from .services.utils import get_safe_methods, get_user_id


# Create your views here.

class JobViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                 mixins.ListModelMixin, mixins.UpdateModelMixin,
                 GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = JobSerializer
    http_method_names = [*get_safe_methods(SAFE_METHODS), "patch", "post"]

    def get_queryset(self):
        user_id = get_user_id(self.request)
        queryset = self.queryset.filter(worker=user_id)
        return queryset

    @action(detail=False, methods=['get'], url_path='all', url_name='all')
    def all_tasks(self, request):
        pk = request.GET.get('pk')
        queryset = self.queryset
        if pk:
            queryset = queryset.filter(pk=pk)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, url_path='create', url_name='create')
    def create_job(self, request):
        serializer = JobCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, mixins.UpdateModelMixin,
                  GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = [*get_safe_methods(SAFE_METHODS), "put", "post"]
    permission_classes = (IsCustomer, )

    def get_queryset(self):
        user_id = get_user_id(self.request)
        queryset = self.queryset.filter(customer=user_id)
        return self.queryset.filter(customer=user_id)

# class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
#                   GenericViewSet):
#
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.type == 'customer':
#             return self.queryset.filter(customer=user.id)
#
#         if user.type == 'worker':
#             return self.queryset.filter(worker=user.id)
#
#         return super().get_queryset()
#
#     def get_serializer_class(self):
#         req_method = self.request.method
#         if req_method == "POST":
#             user = self.request.user
#             if user.type == 'customer':
#                 return CustomerTaskCreateSerializer
#
#             if user.type == 'worker':
#                 return WorkerTaskCreateSerializer
#
#         if req_method in ["PUT", "PATCH"]:
#             print(1)
#             return TaskUpdateSerializer
#
#         return super().get_serializer_class()
#
#     @action(detail=False, methods=['get'], url_path='all', url_name='all')
#     def all_tasks(self, request):
#         serializer = self.get_serializer(self.get_queryset(), many=True)
#         return Response(serializer.data)


# @action(methods=['putch'], detail=True, url_path='close', url_name='close')
# def close_task(self, request, pk=None):

# def get_permissions(self):
#     if self.action == 'update':
