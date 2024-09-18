from rest_framework import mixins
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import GenericViewSet


from .models import *
from .serializers import *
from .permissions import IsSuperWorker, IsSuperCustomer, IsSuperWorkerOrReadOnly


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):

    def get_serializer_class(self):
        request_method = self.request.method
        if request_method not in SAFE_METHODS:
            return UserCreateSerializer

        return super().get_serializer_class()


class WorkerViewSet(UsersViewSet):
    queryset = User.objects.filter(type='worker')
    serializer_class = UserWorkerSerializer
    permission_classes = [IsSuperCustomer | IsSuperWorkerOrReadOnly]


class CustomersViewSet(UsersViewSet):
    queryset = User.objects.filter(type='customer')
    serializer_class = UserCustomerSerializer
    permission_class = IsSuperWorker
#
#
# class NewUsersViewSet(mixins.CreateModelMixin,
#                       mixins.ListModelMixin,
#                       mixins.RetrieveModelMixin,
#                       GenericViewSet):
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.type == "customer":
#             return User.objects.filter(type='customer')
#
#         if user.type == "worker":
#             return User.objects.filter(type='worker')
#
#     def get_serializer_class(self):
#         request = self.request
#         request_method = request.method
#         if request_method not in SAFE_METHODS:
#             return UserCreateSerializer
#
#         user = request.method
#         if user.type == "customer":
#             return UserCustomerSerializer
#
#         if user.type == "worker":
#             return UserWorkerSerializer
#
#         return super().get_serializer_class()
