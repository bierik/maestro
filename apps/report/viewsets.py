from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.report.models import Report
from apps.report.serializers import ReportSerializer


class ReportViewset(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
):
    queryset = Report.objects.order_by("-created")
    serializer_class = ReportSerializer

    @action(detail=False)
    def running(self, request):
        running = Report.running()
        if running is None:
            return Response(None)
        return Response(ReportSerializer(Report.running()).data)
