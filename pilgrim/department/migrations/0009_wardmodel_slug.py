# Generated by Django 5.0.2 on 2024-04-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0008_alter_bedmodel_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='wardmodel',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='Слаг'),
        ),
    ]