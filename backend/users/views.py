from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from services.mixins.permissions import SelectPermissionByActionMixin
from .serializers import *
from .permissions import IsUserAccount, IsSuperWorker, IsSuperCustomerReadWorkers


class CRViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    pass


class UsersViewSet(SelectPermissionByActionMixin, CRViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']
    permission_classes_by_action = {
        'list': [IsSuperWorker | IsSuperCustomerReadWorkers],
        'retrieve': [IsUserAccount | IsSuperWorker | IsSuperCustomerReadWorkers],
        'create': [IsSuperWorker]
    }
