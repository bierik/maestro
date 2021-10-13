from django.contrib import admin

from apps.flat.models import Flat, FlatTemplate


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    pass


@admin.register(FlatTemplate)
class FlatTemplateAdmin(admin.ModelAdmin):
    pass
