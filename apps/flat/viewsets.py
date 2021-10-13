from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from apps.flat.models import Flat, FlatTemplate
from apps.flat.serializers import FlatSerializer, FlatTemplateSerializer


class FlatViewset(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
):
    queryset = Flat.objects.order_by("-created")
    serializer_class = FlatSerializer


class FlatTemplateViewset(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin
):
    queryset = FlatTemplate.objects.order_by("name")
    serializer_class = FlatTemplateSerializer
