# Generated by Django 3.2 on 2021-05-02 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="sex",
            field=models.CharField(
                choices=[("MALE", "Männlich"), ("FEMALE", "Weiblich")],
                default="MALE",
                max_length=255,
                verbose_name="Geschlecht",
            ),
        ),
    ]
