from pluck import pluck
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.customer.models import Address, Customer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "address", "zip_code", "place", "is_primary", "route_flat")


class SimpleCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "price_per_hour",
            "color",
        )
        read_only_fields = ("full_name", "primary_address")


class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    primary_address = AddressSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "company",
            "price_per_hour",
            "color",
            "addresses",
            "primary_address",
            "is_active",
        )
        read_only_fields = ("full_name", "primary_address")

    def create(self, validated_data):
        addresses = validated_data.pop("addresses")
        primary_addresses = list(
            filter(lambda address: address.get("is_primary", False), addresses)
        )

        if len(primary_addresses) > 1:
            raise ValidationError("There are more than one primary address")

        # Mark the first address as primary is not already set
        if len(addresses) > 0 and len(primary_addresses) == 0:
            addresses[0]["is_primary"] = True

        customer = Customer.objects.create(**validated_data)

        for address in addresses:
            address["customer_id"] = customer.id
            Address.objects.create(**address)

        return customer

    def update(self, customer, validated_data):
        addresses = validated_data.pop("addresses")
        primary_addresses = filter(
            lambda address: address.get("is_primary", False), addresses
        )

        if len(list(primary_addresses)) > 1:
            raise ValidationError("There are more than one primary address")

        customer = super().update(customer, validated_data)

        customer.addresses.exclude(id__in=pluck(addresses, "id", default=None)).delete()

        for address in addresses:
            address["customer_id"] = customer.id
            Address.objects.update_or_create(id=address.get("id"), defaults=address)

        return customer

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        company = attrs.get("company")
        if not company and last_name and first_name:
            return attrs
        if not last_name and not first_name and company:
            return attrs
        raise ValidationError(
            _(
                "Es muss entweder ein Vor- und Nachname oder eine Firma eingegeben werden."  # noqa
            )
        )
