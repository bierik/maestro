import arrow
from django.conf import settings
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from customer.models import Customer
from invoice.models import Invoice
from invoice.serializers import InvoiceSerializer
from invoice.services import InvoiceService


class InvoiceViewset(
    GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin
):
    queryset = Invoice.objects.order_by("-created").all()
    serializer_class = InvoiceSerializer

    def filter_queryset(self, queryset):
        status_filter = self.request.query_params.getlist("status")
        return queryset.filter(status__in=status_filter)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.data["customer"])
        start = arrow.get(request.data["start"], tzinfo=settings.TIME_ZONE).date()
        end = (
            arrow.get(request.data["end"], tzinfo=settings.TIME_ZONE)
            .shift(days=1)
            .date()
        )
        invoice_service = InvoiceService(customer=customer, start=start, end=end)
        invoice_service.generate_invoice()
        return Response()

    @action(detail=True, methods=["POST"])
    def send(self, request, pk=None):
        invoice = Invoice.objects.get(id=pk)
        invoice.send()
        return Response()

    @action(detail=True, methods=["POST"])
    def pay(self, request, pk=None):
        invoice = Invoice.objects.get(id=pk)
        invoice.pay()
        return Response()

    @action(detail=True, methods=["POST"])
    def archive(self, request, pk=None):
        invoice = Invoice.objects.get(id=pk)
        invoice.archive()
        return Response()
