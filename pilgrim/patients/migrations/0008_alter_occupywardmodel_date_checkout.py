# Generated by Django 5.0.2 on 2024-04-15 18:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0007_occupywardmodel_operation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupywardmodel',
            name='date_checkout',
            field=models.DateField(default=datetime.date(2024, 4, 18), null=True, verbose_name='Дата выселения'),
        ),
    ]
