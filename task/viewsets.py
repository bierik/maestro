from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from task.models import Task
from task.serializers import TaskSerializer
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from customer.serializers import NextEventSerializer


class TaskViewset(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False)
    def next_event(self, request):
        tasks = Task.objects.all()
        if not tasks.exists():
            return None
        events = [
            {"datetime": task.rrule.after(timezone.now()), "task": task}
            for task in list(tasks)
        ]
        events = sorted(events, key=lambda event: event["datetime"])
        next_event = events[0]
        next_event_serializer = NextEventSerializer(
            data={
                "next_event": next_event["datetime"],
                "customer": next_event["task"].customer.id,
            }
        )
        next_event_serializer.is_valid(raise_exception=True)
        return Response(next_event_serializer.data)
