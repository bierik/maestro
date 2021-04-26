from django.contrib import admin

from invoice.models import HistoryEntry, Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(HistoryEntry)
class HistoryEntryAdmin(admin.ModelAdmin):
    pass
