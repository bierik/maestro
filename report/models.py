from django.db import models
from django_extensions.db.models import TimeStampedModel

from customer.models import Customer


class Report(TimeStampedModel):
    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapporte"

    start = models.DateTimeField(verbose_name="Startzeit")
    end = models.DateTimeField(verbose_name="Endzeit", null=True)
    title = models.CharField(verbose_name="Titel", max_length=255)
    route_flat = models.BooleanField(verbose_name="Wegpauschale", default=True)
    customer = models.ForeignKey(
        Customer, verbose_name="Kunde", on_delete=models.CASCADE, related_name="reports"
    )

    @classmethod
    def running(cls):
        return cls.objects.filter(end__isnull=True).first()

    def _rounded_hours_decimal(self):
        hours_decimal = (self.end - self.start).seconds / 3600
        return round(hours_decimal * 4) / 4

    def duration(self):
        rounded_hours_decimal = self._rounded_hours_decimal()
        hours = int(rounded_hours_decimal)
        minutes = int((rounded_hours_decimal * 60) % 60)
        return (hours, minutes)

    def price(self):
        rounded_hours_decimal = self._rounded_hours_decimal()
        return float(self.customer.price_per_hour) * rounded_hours_decimal
