from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from report.models import Report
from report.serializers import ReportSerializer
from rest_framework.response import Response


class ReportViewset(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=False)
    def running(self, request):
        running = Report.running()
        if running is None:
            return Response(None)
        return Response(ReportSerializer(Report.running()).data)
