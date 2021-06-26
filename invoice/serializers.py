from rest_framework import serializers

from customer.serializers import SimpleCustomerSerializer
from invoice.models import HistoryEntry, Invoice


class HistoryEntrySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display")

    class Meta:
        model = HistoryEntry
        fields = ("id", "created", "status", "status_display")


class InvoiceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    customer = SimpleCustomerSerializer()
    history = HistoryEntrySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display")

    class Meta:
        model = Invoice
        fields = (
            "id",
            "date",
            "url",
            "customer",
            "number",
            "created",
            "history",
            "status",
            "status_display",
        )

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.file.url)
