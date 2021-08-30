from invoice.models import HistoryStatus
from django_filters import widgets
from django_filters import rest_framework as filters
from invoice.models import Invoice


class InvoiceFilter(filters.FilterSet):
    status = filters.MultipleChoiceFilter(
        choices=HistoryStatus.choices, widget=widgets.CSVWidget
    )

    class Meta:
        model = Invoice
        fields = ["status"]
