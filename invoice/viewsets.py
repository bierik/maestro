import arrow
from django.conf import settings
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from django.http import FileResponse
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
        if not status_filter:
            return queryset
        return queryset.filter(status__in=status_filter)

    def get_invoice_service(self, customer, start, end):
        customer = Customer.objects.get(id=customer)
        start = arrow.get(start, tzinfo=settings.TIME_ZONE).date()
        end = arrow.get(end, tzinfo=settings.TIME_ZONE).shift(days=1).date()
        return InvoiceService(customer=customer, start=start, end=end)

    @transaction.atomic
    def create(self, request):
        data = request.data
        invoice_service = self.get_invoice_service(
            data["customer"], data["start"], data["end"]
        )
        invoice_service.persist_invoice()
        return Response()

    @transaction.atomic
    @action(detail=False, methods=["GET"])
    def preview(self, request):
        data = request.query_params
        invoice_service = self.get_invoice_service(
            data["customer"], data["start"], data["end"]
        )
        invoice = invoice_service.preview_invoice()
        pdf_file = invoice["pdf_file"]
        response = FileResponse(open(pdf_file.name, "rb"))
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

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
