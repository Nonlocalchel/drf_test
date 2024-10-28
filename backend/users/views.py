from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from services.mixins.permissions import SelectPermissionByActionMixin
from services.viewsets import CRViewSet

from .serializers import *
from .permissions import IsUserAccount, IsSuperWorker, IsSuperCustomerReadWorkers
from .utils import get_user_types, format_data_dict


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
        current_user_id = self.kwargs['pk']
        user = request.user
        if current_user_id != str(user.id):
            return super().retrieve(request, *args, **kwargs)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        # format_data_dict(data)
        return super().create(request, *args, **kwargs)
