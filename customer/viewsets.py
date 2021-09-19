from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from customer.models import Customer
from customer.serializers import CustomerSerializer
from flat.models import Flat
from flat.serializers import FlatSerializer
from invoice.filters import InvoiceFilter
from invoice.models import Invoice
from invoice.serializers import InvoiceSerializer
from report.filters import ReportFilter
from report.models import Report
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


class CustomerInvoiceViewset(GenericViewSet, ListModelMixin):
    queryset = Invoice.objects.order_by("-created").all()
    serializer_class = InvoiceSerializer
    filterset_class = InvoiceFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(customer_id=self.kwargs["customer_pk"])


class CustomerFlatViewset(GenericViewSet, ListModelMixin):
    queryset = Flat.objects.order_by("-created").all()
    serializer_class = FlatSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(customer_id=self.kwargs["customer_pk"])


class CustomerReportViewset(GenericViewSet, ListModelMixin):
    pagination_class = None
    queryset = Report.objects.order_by("start").all()
    serializer_class = ReportSerializer
    filterset_class = ReportFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(customer_id=self.kwargs["customer_pk"])
