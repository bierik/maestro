from rest_framework import serializers

from apps.customer.models import Customer
from apps.customer.serializers import SimpleCustomerSerializer
from apps.task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), write_only=True, source="customer"
    )
    rrule_string = serializers.CharField(source="rrule", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "duration",
            "title",
            "rrule",
            "rrule_string",
            "customer",
            "customer_id",
        )
