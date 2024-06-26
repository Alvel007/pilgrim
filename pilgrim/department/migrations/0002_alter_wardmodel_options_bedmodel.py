# Generated by Django 5.0.2 on 2024-04-12 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wardmodel',
            options={'verbose_name': 'Палата', 'verbose_name_plural': 'Палаты'},
        ),
        migrations.CreateModel(
            name='BedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=64, verbose_name='Номер койки')),
                ('ward', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='department.wardmodel', verbose_name='Находится в палате')),
            ],
            options={
                'verbose_name': 'Койка',
                'verbose_name_plural': 'Койки',
            },
        ),
    ]
