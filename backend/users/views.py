from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from services.mixins.permissions import SelectPermissionByActionMixin
from services.viewsets import CRViewSet

from .serializers import *
from .permissions import IsUserAccount, IsSuperWorker, IsSuperCustomerReadWorkers
from .utils import get_user_types


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
        types = get_user_types()
        return self.queryset.select_related(*types)

    def retrieve(self, request, *args, **kwargs):
        # user = request.user.prefetch_related('worker__exp')
        # user = User.objects.all(request.user)
        # req_user =
        user = request.user
        # user = User.objects.get(id=re)
        # user['customer'] = customer_data
        # print(request)
        # return super().retrieve(request, *args, **kwargs)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
