# Generated by Django 3.2.9 on 2022-03-19 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20220319_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Aktiv'),
        ),
    ]
