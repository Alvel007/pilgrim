# Generated by Django 5.0.2 on 2024-04-15 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_occupywardmodel_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='occupywardmodel',
            name='operation',
            field=models.BooleanField(default=False, verbose_name='Операция'),
        ),
    ]