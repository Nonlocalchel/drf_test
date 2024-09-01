from django.forms import model_to_dict
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from tasks.services.utils import get_safe_methods
from .models import *
from .serializers import *
from .permissions import IsSuperWorker, IsSuperCustomer, IsSuperWorkerOrReadOnly


# Create your views here.
# class UserViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     @action(methods=['get', 'post'], detail=False)
#     def workers(self, request, pk=None):
#         workers = User.objects.filter(type='worker')
#         return Response(UserWorkerSerializer(workers, many=True).data)
#
#     @action(methods=['get', 'post'], detail=False)
#     def customers(self, request, pk=None):
#         customers = User.objects.filter(type='customer')
#         return Response(UserCustomerSerializer(customers, many=True).data)

class UsersViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass


class WorkerViewSet(UsersViewSet):
    queryset = User.objects.filter(type='worker')
    serializer_class = UserWorkerSerializer
    permission_classes = [IsSuperCustomer | IsSuperWorkerOrReadOnly]


class CustomersViewSet(UsersViewSet):
    queryset = User.objects.filter(type='customer')
    serializer_class = UserCustomerSerializer
    permission_classes = (IsSuperWorker, IsSuperWorkerOrReadOnly)

    def get_serializer_class(self):
        if self.action not in get_safe_methods():
            return UserCreateSerializer

        return super().get_serializer_class()
