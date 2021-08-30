from django_filters import rest_framework as filters
from report.models import Report


class ReportFilter(filters.FilterSet):
    start = filters.DateTimeFilter(lookup_expr="gte")
    end = filters.DateTimeFilter(lookup_expr="lte")

    class Meta:
        model = Report
        fields = ["start", "end"]
