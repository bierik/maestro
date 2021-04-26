from rest_framework import serializers

from customer.models import Customer
from customer.serializers import SimpleCustomerSerializer
from task.models import Task


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
