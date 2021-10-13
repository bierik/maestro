from django.contrib import admin

from apps.invoice.models import HistoryEntry, Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(HistoryEntry)
class HistoryEntryAdmin(admin.ModelAdmin):
    pass
