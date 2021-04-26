from django.contrib import admin

from customer.models import Address, Customer


class AddressInline(admin.StackedInline):
    model = Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering = ["last_name", "first_name"]
    search_fields = ["last_name", "first_name"]
    inlines = [AddressInline]
