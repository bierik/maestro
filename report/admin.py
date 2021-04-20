from django.contrib import admin
from report.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
