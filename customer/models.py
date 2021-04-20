from django.db import models
from django_extensions.db.models import TimeStampedModel
from colorfield.fields import ColorField


class Customer(TimeStampedModel):
    class Meta:
        verbose_name = "Kunde"
        verbose_name_plural = "Kunden"

    first_name = models.CharField(verbose_name="Vorname", max_length=255)
    last_name = models.CharField(verbose_name="Nachname", max_length=255)
    price_per_hour = models.DecimalField(
        verbose_name="Stundenansatz", decimal_places=2, max_digits=5
    )
    color = ColorField(default="#1976d2")

    @property
    def full_name(self):
        return " ".join([self.last_name, self.first_name])

    @property
    def primary_address(self):
        return self.addresses.filter(is_primary=True).first()

    def __str__(self):
        return self.full_name


class Address(models.Model):
    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adressen"

    address = models.CharField(verbose_name="Adresse", max_length=255)
    zip_code = models.CharField(verbose_name="Postleitzahl", max_length=4)
    place = models.CharField(verbose_name="Ort", max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="addresses"
    )
    is_primary = models.BooleanField(verbose_name="Primäradresse", default=False)

    def __str__(self):
        return f"{self.address}, {self.zip_code} {self.place}"
