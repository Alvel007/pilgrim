# Generated by Django 5.0.2 on 2024-04-20 07:50

import colorful.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0012_alter_occupywardmodel_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupywardmodel',
            name='color',
            field=colorful.fields.RGBColorField(default='#8B0000', help_text='Выберите цвет заливки для пациента', verbose_name='Цвет заливки'),
        ),
        migrations.AlterField(
            model_name='occupywardmodel',
            name='date_checkout',
            field=models.DateField(default=datetime.date(2024, 4, 23), null=True, verbose_name='Дата выселения'),
        ),
    ]
