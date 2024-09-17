from http import HTTPMethod

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from services.viewsets_classes import SelectPermissionByActionMixin
from users.permissions import IsWorker, IsSuperWorker, IsCustomer
from users.services.utils import get_user_id
from .filters import TaskFilter
from .models import Task
from .serializers import (
    TaskReadSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskPartialUpdateSerializer
)

from .services.utils import *
from .validators import validate_type_field


# Create your views here.
class CRUViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, mixins.UpdateModelMixin,
                  GenericViewSet):
    pass


class TaskViewSet(CRUViewSet, SelectPermissionByActionMixin):
    queryset = Task.objects.all()
    serializer_class = TaskReadSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['worker', 'customer', 'status']
    filterset_class = TaskFilter
    permission_classes_by_action = None

    def get_permissions(self):
        req_method = self.request.method
        if req_method == HTTPMethod.GET:
            "огика будет отдавать прва в зависимомти от запроса.Дальше права буду проверять тип пользователя"
            return [permission() for permission in self.permission_classes]

        return super().get_permissions()

    def get_serializer_class(self):
        serializer_classes_by_action = {
            'get': TaskReadSerializer,
            'post': TaskCreateSerializer,
            'put': TaskUpdateSerializer,
            'patch': TaskPartialUpdateSerializer
        }

        req_method = self.request.method.lower()
        serializer_class = serializer_classes_by_action[req_method]
        return serializer_class

    # def get_queryset(self):
    #     queryset = self.queryset
    #     user = self.request.user
    #     user_id = user.id
    #     if user.type == 'customer':
    #         return get_customer_queryset(queryset, user_id)
    #
    #     return get_worker_queryset(queryset, user_id)

    # @action(detail=False, methods=[HTTPMethod.GET], url_path='all', permission_classes=[IsSuperWorker])
    # def all_tasks(self, request):
    #     pk = request.GET.get('pk')
    #     queryset = self.queryset
    #     if pk:
    #         queryset = queryset.filter(pk=pk)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     user_type = user.type
    #     validate_type_field(user_type, serializer.data.user.customer)
    #     if user_type == 'customer':
    #         serializer.validated_data['customer'] = user.customer
    #
    #     serializer.save()


# class JobViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
#                  mixins.ListModelMixin, mixins.UpdateModelMixin,
#                  GenericViewSet):
#     queryset = Task.objects.all()
#     serializer_class = JobSerializer
#     http_method_names = [*get_safe_methods(), "patch", "post"]
#     permission_classes = (IsAuthenticated, IsWorker,)
#
#     def get_queryset(self):
#         request = self.request
#         user_id = get_user_id(request)
#
#         queryset = super().get_queryset()
#         query_type = request.GET.get("q")
#
#         return get_job_query(queryset, query_type, user_id)
#
#     @action(detail=False, methods=[HTTPMethod.GET], url_path='all', permission_classes=[IsSuperWorker])
#     def all_tasks(self, request):
#         pk = request.GET.get('pk')
#         queryset = self.queryset
#         if pk:
#             queryset = queryset.filter(pk=pk)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     @action(methods=[HTTPMethod.POST], detail=False, url_path='create', permission_classes=[IsSuperWorker])
#     def create_job(self, request):
#         serializer = JobCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#
# class TaskViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
#                   mixins.ListModelMixin, mixins.UpdateModelMixin,
#                   GenericViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     http_method_names = [*get_safe_methods(), "put", "post"]
#     permission_classes = (IsAuthenticated, IsCustomer, )
#
#     def get_queryset(self):
#         user_id = get_user_id(self.request)
#         queryset = self.queryset.filter(customer=user_id)
#         return queryset

