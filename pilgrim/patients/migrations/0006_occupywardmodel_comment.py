# Generated by Django 5.0.2 on 2024-04-14 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_occupywardmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='occupywardmodel',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
    ]
