from rest_framework import serializers

from apps.customer.models import Customer
from apps.customer.serializers import SimpleCustomerSerializer
from apps.flat.models import Flat, FlatTemplate


class FlatSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), write_only=True, source="customer"
    )

    class Meta:
        model = Flat
        fields = (
            "id",
            "name",
            "price",
            "customer",
            "customer_id",
            "created",
        )


class FlatInvoiceSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Flat
        fields = (
            "name",
            "price",
            "amount",
            "total",
        )

    def get_amount(self, obj):
        return "1"

    def get_total(self, obj):
        return "{:.2f} CHF".format(obj.price)

    def get_price(self, obj):
        return "{:.2f} CHF".format(obj.price)


class FlatTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatTemplate
        fields = (
            "id",
            "name",
            "price",
        )
