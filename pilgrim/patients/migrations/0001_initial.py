# Generated by Django 5.0.2 on 2024-04-13 15:59

import colorful.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=64, verbose_name='Отчество')),
                ('telephone', models.CharField(blank=True, max_length=64, verbose_name='Телефон')),
                ('slug', models.SlugField(editable=False, unique=True, verbose_name='Слаг')),
                ('color', colorful.fields.RGBColorField(default='#FFFFFF', help_text='Выберите цвет заливки для пациента', verbose_name='Цвет заливки')),
            ],
            options={
                'verbose_name': 'Пациент',
                'verbose_name_plural': 'Пациенты',
            },
        ),
    ]