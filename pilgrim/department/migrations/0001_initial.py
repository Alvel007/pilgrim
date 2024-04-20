# Generated by Django 5.0.2 on 2024-02-20 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название отделения')),
                ('address', models.CharField(max_length=128, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Отделение',
                'verbose_name_plural': 'Отделения',
            },
        ),
        migrations.CreateModel(
            name='WardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование палаты')),
                ('department', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='department.departmentmodel', verbose_name='Находится в отделении')),
            ],
        ),
    ]