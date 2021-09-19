# Generated by Django 3.2 on 2021-09-18 20:38

import django.db.models.deletion
import django_extensions.db.fields
import recurrence.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("title", models.CharField(max_length=255, verbose_name="Titel")),
                ("duration", models.DurationField(verbose_name="Dauer")),
                ("rrule", recurrence.fields.RecurrenceField(verbose_name="rrule")),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="customer.customer",
                        verbose_name="Kunde",
                    ),
                ),
            ],
            options={
                "verbose_name": "Auftrag",
                "verbose_name_plural": "Aufträge",
            },
        ),
    ]
