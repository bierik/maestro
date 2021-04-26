from django.db import models
from django_extensions.db.models import TimeStampedModel
from recurrence.fields import RecurrenceField

from customer.models import Customer


class Task(TimeStampedModel):
    class Meta:
        verbose_name = "Auftrag"
        verbose_name_plural = "Aufträge"

    title = models.CharField(verbose_name="Titel", max_length=255)
    duration = models.DurationField(verbose_name="Dauer")
    rrule = RecurrenceField(verbose_name="rrule")
    customer = models.ForeignKey(
        Customer,
        verbose_name="Kunde",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
