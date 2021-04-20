from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from customer.models import Customer
from customer.serializers import CustomerSerializer
from report.serializers import ReportSerializer


class CustomerViewset(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
):
    queryset = Customer.objects.order_by("last_name", "first_name")
    serializer_class = CustomerSerializer

    @action(detail=True)
    def reports(self, request, pk):
        customer = Customer.objects.get(id=pk)
        reports_serializer = ReportSerializer(
            instance=customer.reports.order_by("-start"), many=True
        )
        return Response(reports_serializer.data)
