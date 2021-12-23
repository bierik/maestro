from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from apps.api.mixins import SerializerActionMixin

from apps.customer.serializers import NextEventSerializer
from apps.task.models import Task
from apps.task.serializers import TaskSerializer
from apps.task.serializers import TaskCreateSerializer


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

    @action(detail=False)
    def next_event(self, request):
        tasks = Task.objects.all()
        if not tasks.exists():
            return Response(None)
        events = [
            {"datetime": task.rrule.after(timezone.now()), "task": task}
            for task in list(tasks)
        ]
        events = sorted(events, key=lambda event: event["datetime"])
        next_event = events[0]
        next_event_serializer = NextEventSerializer(
            data={
                "next_event": next_event["datetime"],
                "next_event_title": next_event["task"].title,
                "customer": next_event["task"].customer.id,
            }
        )
        next_event_serializer.is_valid(raise_exception=True)
        return Response(next_event_serializer.data)
