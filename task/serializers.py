from rest_framework import serializers
from task.models import Task
from customer.serializers import SimpleCustomerSerializer


class TaskSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer()
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
        )
