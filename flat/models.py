from django.db import models
from django_extensions.db.models import TimeStampedModel

from customer.models import Customer


class Flat(TimeStampedModel):
    class Meta:
        verbose_name = "Pauschal"
        verbose_name_plural = "Pauschale"

    name = models.CharField(verbose_name="Name", max_length=255)
    price = models.DecimalField(verbose_name="Preis", decimal_places=2, max_digits=5)
    customer = models.ForeignKey(
        Customer, verbose_name="Kunde", on_delete=models.CASCADE, related_name="flats"
    )


class FlatTemplate(models.Model):
    class Meta:
        verbose_name = "Pauschalvorlage"
        verbose_name_plural = "Pauschalvorlagen"

    name = models.CharField(verbose_name="Name", max_length=255)
    price = models.DecimalField(verbose_name="Preis", decimal_places=2, max_digits=5)
