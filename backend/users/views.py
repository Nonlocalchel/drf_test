from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializers import *
from .permissions import IsSuperWorkerOrReadOnly


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # [IsSuperWorkerOrReadOnly]
    serializer_class = UserSerializer
