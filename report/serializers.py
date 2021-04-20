from rest_framework import serializers
from report.models import Report
from customer.models import Customer
from customer.serializers import SimpleCustomerSerializer


class ReportSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), write_only=True, source="customer"
    )

    class Meta:
        model = Report
        fields = ("id", "start", "end", "title", "customer", "customer_id")
