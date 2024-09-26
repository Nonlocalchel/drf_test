from rest_framework import mixins
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializers import *
from .permissions import IsSuperWorker, IsSuperCustomer, IsSuperWorkerOrReadOnly


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # [IsSuperWorkerOrReadOnly]
    serializer_class = UserSerializer
