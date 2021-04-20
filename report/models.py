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
    customer = models.ForeignKey(
        Customer, verbose_name="Kunde", on_delete=models.CASCADE, related_name="reports"
    )

    @classmethod
    def running(cls):
        return cls.objects.filter(end__isnull=True).first()
