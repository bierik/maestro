# Generated by Django 3.2 on 2021-05-05 13:02

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0002_alter_invoice_customer"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoryEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CREATED", "Erstellt"),
                            ("SENT", "Versendet"),
                            ("PAYED", "Bezahlt"),
                            ("DELETED", "Gelöscht"),
                            ("ARCHIVED", "Archiviert"),
                        ],
                        default="CREATED",
                        max_length=255,
                        verbose_name="Status",
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="history",
                        to="invoice.invoice",
                        verbose_name="Rechnung",
                    ),
                ),
            ],
            options={
                "verbose_name": "Verlaufeintrag",
                "verbose_name_plural": "Verlaufeinträge",
            },
        ),
    ]
