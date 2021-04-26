# Generated by Django 3.2 on 2021-05-05 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20210505_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Erstellt'), ('SENT', 'Versendet'), ('PAYED', 'Bezahlt'), ('ARCHIVED', 'Archiviert')], default='CREATED', max_length=255, verbose_name='Status'),
        ),
    ]
