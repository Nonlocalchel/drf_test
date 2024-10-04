from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CRViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    pass


class CRUViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                 mixins.ListModelMixin, mixins.UpdateModelMixin,
                 GenericViewSet):
    pass
