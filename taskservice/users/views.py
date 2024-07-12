from django.forms import model_to_dict
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializer import *


# Create your views here.
class UserViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get', 'post'], detail=False)
    def workers(self, request, pk=None):
        workers = User.objects.filter(type='worker')
        return Response(UserWorkerSerializer(workers, many=True).data)

    @action(methods=['get', 'post'], detail=False)
    def customers(self, request, pk=None):
        customers = User.objects.filter(type='customer')
        return Response(UserCustomerSerializer(customers, many=True).data)

