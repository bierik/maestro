from django.contrib import admin
from customer.models import Customer
from customer.models import Address


class AddressInline(admin.StackedInline):
    model = Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering = ["last_name", "first_name"]
    search_fields = ["last_name", "first_name"]
    inlines = [AddressInline]
