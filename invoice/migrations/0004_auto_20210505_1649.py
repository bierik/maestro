# Generated by Django 3.2 on 2021-05-05 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0003_historyentry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historyentry",
            name="invoice",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="historyentries",
                to="invoice.invoice",
                verbose_name="Rechnung",
            ),
        ),
        migrations.AlterField(
            model_name="historyentry",
            name="status",
            field=models.CharField(
                choices=[
                    ("CREATED", "Erstellt"),
                    ("SENT", "Versendet"),
                    ("PAYED", "Bezahlt"),
                    ("ARCHIVED", "Archiviert"),
                ],
                default="CREATED",
                max_length=255,
                verbose_name="Status",
            ),
        ),
    ]
