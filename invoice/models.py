from django.db import models
from django_extensions.db.models import TimeStampedModel

from customer.models import Customer


class HistoryStatus(models.TextChoices):
    CREATED = "CREATED", "Erstellt"
    SENT = "SENT", "Versendet"
    PAYED = "PAYED", "Bezahlt"
    ARCHIVED = "ARCHIVED", "Archiviert"


class Invoice(TimeStampedModel):
    class Meta:
        verbose_name = "Rechnung"
        verbose_name_plural = "Rechnungen"

    customer = models.ForeignKey(
        Customer,
        verbose_name="Kunde",
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    file = models.FileField()
    source_file = models.FileField()
    date = models.DateField()
    status = models.CharField(
        verbose_name="Status",
        max_length=255,
        choices=HistoryStatus.choices,
        default=HistoryStatus.CREATED,
    )

    def history(self):
        return self.historyentries.order_by("-created")

    def number(self):
        return f"{self.id}/{self.date.year}"

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.history().exists():
            HistoryEntry.objects.create(invoice_id=self.id)

    def _apply_status(self, status):
        self.historyentries.add(
            HistoryEntry.objects.create(invoice_id=self.id, status=status)
        )
        self.status = status
        self.save()

    def send(self):
        self._apply_status(HistoryStatus.SENT)

    def pay(self):
        self._apply_status(HistoryStatus.PAYED)

    def archive(self):
        self._apply_status(HistoryStatus.ARCHIVED)


class HistoryEntry(TimeStampedModel):
    class Meta:
        verbose_name = "Verlaufeintrag"
        verbose_name_plural = "Verlaufeinträge"

    invoice = models.ForeignKey(
        Invoice,
        verbose_name="Rechnung",
        on_delete=models.CASCADE,
        related_name="historyentries",
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=255,
        choices=HistoryStatus.choices,
        default=HistoryStatus.CREATED,
    )
