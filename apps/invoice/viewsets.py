from django.db import transaction

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.invoice.filters import InvoiceFilter
from apps.invoice.models import Invoice
from apps.invoice.serializers import InvoiceSerializer
from apps.invoice.services import InvoiceService


class InvoiceViewset(
    GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin
):
    queryset = Invoice.objects.order_by("-created").all()
    serializer_class = InvoiceSerializer
    filterset_class = InvoiceFilter

    @transaction.atomic
    def create(self, request):
        invoice_service = InvoiceService.from_data(request.data)
        invoice_service.persist_invoice()
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
