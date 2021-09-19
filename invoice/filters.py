from django_filters import rest_framework as filters
from django_filters import widgets

from invoice.models import HistoryStatus, Invoice


class InvoiceFilter(filters.FilterSet):
    status = filters.MultipleChoiceFilter(
        choices=HistoryStatus.choices, widget=widgets.CSVWidget
    )

    class Meta:
        model = Invoice
        fields = ["status"]
