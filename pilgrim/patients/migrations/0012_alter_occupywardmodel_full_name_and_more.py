# Generated by Django 5.0.2 on 2024-04-19 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0011_remove_occupywardmodel_patient_occupywardmodel_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupywardmodel',
            name='full_name',
            field=models.CharField(max_length=64, verbose_name='Фамилия И.О.'),
        ),
        migrations.AlterField(
            model_name='occupywardmodel',
            name='slug',
            field=models.SlugField(editable=False, unique=True, verbose_name='Слаг'),
        ),
    ]
