from django_filters.rest_framework import DjangoFilterBackend

from services.mixins.permissions import SelectPermissionByActionMixin
from services.viewsets import CRViewSet

from .serializers import *
from .permissions import IsUserAccount, IsSuperWorker, IsSuperCustomerReadWorkers


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

    def get_queryset(self):
        # super().get_queryset()
        types = [user_type.value for user_type in User.UserType]
        return self.queryset.select_related(*types)
