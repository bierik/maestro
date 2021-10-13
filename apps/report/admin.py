from django.contrib import admin

from apps.report.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
