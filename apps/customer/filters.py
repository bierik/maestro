from django.db.models import TextField, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters

from apps.customer.models import Customer


class CustomerFilter(filters.FilterSet):
    text = filters.CharFilter(method="filter_text")
    is_active = filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = Customer
        fields = ["text", "is_active"]

    def filter_text(self, queryset, name, value):
        return queryset.annotate(
            text=Concat("first_name", Value(" "), "last_name", output_field=TextField())
        ).filter(text__icontains=value)

    def filter_is_active(self, queryset, name, value):
        if value:
            return queryset.exclude(is_active=False)
        return queryset
