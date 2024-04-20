# Generated by Django 5.0.2 on 2024-04-19 22:19

import colorful.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_alter_occupywardmodel_date_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occupywardmodel',
            name='patient',
        ),
        migrations.AddField(
            model_name='occupywardmodel',
            name='color',
            field=colorful.fields.RGBColorField(default='#FFFFFF', help_text='Выберите цвет заливки для пациента', verbose_name='Цвет заливки'),
        ),
        migrations.AddField(
            model_name='occupywardmodel',
            name='full_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Фамилия И.О.'),
        ),
        migrations.AddField(
            model_name='occupywardmodel',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Слаг'),
        ),
        migrations.AddField(
            model_name='occupywardmodel',
            name='telephone',
            field=models.CharField(blank=True, max_length=64, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='occupywardmodel',
            name='date_checkout',
            field=models.DateField(default=datetime.date(2024, 4, 22), null=True, verbose_name='Дата выселения'),
        ),
    ]
