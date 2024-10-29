from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from services.mixins.permissions import SelectPermissionByActionMixin
from services.viewsets import CRViewSet

from .serializers import *
from .permissions import IsUserAccount, IsSuperWorker, IsSuperCustomer
from .utils.views_utils import is_user_account_request, filter_user_queryset, optimize_queryset


class UsersViewSet(SelectPermissionByActionMixin, CRViewSet):
    """Users app view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']
    permission_classes_by_action = {
        'list': [IsSuperWorker | IsSuperCustomer],
        # 'retrieve': [IsUserAccount],# | IsSuperWorker | IsSuperCustomer
        'create': [IsSuperWorker]
    }

    def get_queryset(self):
        """Optimize get users queryset"""
        user = self.request.user
        filtered_queryset = filter_user_queryset(user, self.queryset)
        return optimize_queryset(filtered_queryset)

    def retrieve(self, request, *args, **kwargs):
        """Optimize get user account"""
        user = request.user
        if is_user_account_request(user, self.kwargs['pk']):
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        return super().retrieve(request, *args, **kwargs)

