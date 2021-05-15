from datetime import date

import arrow
from django.conf import settings
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

from customer.models import Customer
from customer.serializers import CustomerSerializer
from flat.serializers import FlatSerializer
from invoice.serializers import InvoiceSerializer
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

    def filter_created(self, queryset, date_filter_string):
        from_date_filter = (
            arrow.get(date_filter_string, tzinfo=settings.TIME_ZONE)
            if date_filter_string
            else date.today()
        )
        to_date_filter = from_date_filter.shift(days=1)
        return queryset.filter(
            created__gte=from_date_filter.datetime,
            created__lte=to_date_filter.datetime,
        )

    @action(detail=True)
    def reports(self, request, pk):
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        customer = Customer.objects.get(id=pk)
        reports_serializer = ReportSerializer(
            customer.reports.filter(start__gte=start, end__lte=end),
            many=True,
        )
        return Response(reports_serializer.data)

    @action(detail=True)
    def flats(self, request, pk):
        date_filter_string = request.query_params.get("date", date.today())
        customer = Customer.objects.get(id=pk)
        flats_serializer = FlatSerializer(
            instance=self.filter_created(
                customer.flats.order_by("-created"), date_filter_string
            ),
            many=True,
        )
        return Response(flats_serializer.data)

    @action(detail=True)
    def invoices(self, request, pk):
        status_filter = request.query_params.getlist("status")
        customer = Customer.objects.get(id=pk)
        invoice_serializer = InvoiceSerializer(
            instance=customer.invoices.order_by("-created").filter(
                status__in=status_filter
            ),
            many=True,
        )
        return Response(invoice_serializer.data)
