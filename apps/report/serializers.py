import arrow
from rest_framework import serializers

from apps.customer.models import Customer
from apps.customer.serializers import SimpleCustomerSerializer
from apps.report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), write_only=True, source="customer"
    )

    class Meta:
        model = Report
        fields = (
            "id",
            "start",
            "end",
            "title",
            "customer",
            "customer_id",
            "route_flat",
        )


class ReportInvoiceSerializer(serializers.ModelSerializer):
    price_per_hour = serializers.SerializerMethodField()
    hours = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ("date", "title", "hours", "price_per_hour", "total")

    def get_hours(self, obj):
        (hours, minutes) = obj.duration()
        hours = str(hours).rjust(2, "0")
        minutes = str(minutes).rjust(2, "0")
        return f"{hours}:{minutes}"

    def get_total(self, obj):
        return "{:.2f} CHF".format(obj.price())

    def get_date(self, obj):
        return arrow.get(obj.created).format("DD.MM.YYYY")

    def get_price_per_hour(self, obj):
        return "{:.2f} CHF".format(obj.customer.price_per_hour)
