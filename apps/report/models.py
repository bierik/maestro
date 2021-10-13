from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.customer.models import Customer


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

    def hours_decimal(self):
        return (self.end - self.start).seconds / 3600

    def duration(self):
        hours_decimal = self.hours_decimal()
        hours = int(hours_decimal)
        minutes = int((hours_decimal * 60) % 60)
        return (hours, minutes)

    def price(self):
        return float(self.customer.price_per_hour) * self.hours_decimal()
