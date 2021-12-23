from rest_framework import serializers

from apps.customer.models import Customer
from apps.customer.serializers import SimpleCustomerSerializer
from apps.task.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source="customer"
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "duration",
            "title",
            "rrule",
            "customer_id",
        )

    # https://github.com/django-recurrence/django-recurrence/issues/158
    def to_internal_value(self, data):
        rrule = data["rrule"]
        if "\nEXDATE:" in rrule:
            rrule, exdates = rrule.split("\nEXDATE:")
            exdates = exdates.split(",")
            rrule += "\nEXDATE:" + "\nEXDATE:".join(exdates)
            data["rrule"] = rrule

        return super().to_internal_value(data)


class TaskSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer()
    rrule_string = serializers.CharField(source="rrule")

    class Meta:
        model = Task
        fields = (
            "id",
            "duration",
            "title",
            "rrule",
            "rrule_string",
            "customer",
        )
