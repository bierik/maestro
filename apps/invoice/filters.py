from django_filters import rest_framework as filters
from django_filters import widgets
from django.db.models import TextField
from django.db.models import Value
from django.db.models.functions import Concat

from apps.invoice.models import HistoryStatus, Invoice


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class InvoiceFilter(filters.FilterSet):
    status = filters.MultipleChoiceFilter(
        choices=HistoryStatus.choices, widget=widgets.CSVWidget
    )
    number = filters.CharFilter(method="filter_number")
    customer = NumberInFilter(field_name="customer_id", lookup_expr="in")
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Invoice
        fields = ["status", "number", "date"]

    def filter_number(self, queryset, name, value):
        return queryset.annotate(
            number=Concat("id", Value("/"), "date__year", output_field=TextField())
        ).filter(number__icontains=value)
