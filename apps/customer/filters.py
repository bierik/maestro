from django.db.models import TextField, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters

from apps.customer.models import Customer


class CustomerFilter(filters.FilterSet):
    text = filters.CharFilter(method="filter_text")

    class Meta:
        model = Customer
        fields = ["text"]

    def filter_text(self, queryset, name, value):
        return queryset.annotate(
            text=Concat("first_name", Value(" "), "last_name", output_field=TextField())
        ).filter(text__icontains=value)
