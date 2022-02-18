from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from apps.api.mixins import SerializerActionMixin
from apps.task.models import Task
from apps.task.serializers import TaskCreateSerializer, TaskSerializer


class TaskViewset(
    SerializerActionMixin,
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
):
    pagination_class = None
    queryset = Task.objects.order_by("title").all()
    serializer_class = TaskSerializer
    serializer_action_classes = {
        "create": TaskCreateSerializer,
        "partial_update": TaskCreateSerializer,
    }
