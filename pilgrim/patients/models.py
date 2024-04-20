import random
import string
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from colorful.fields import RGBColorField
from department.models import BedModel
from django.utils import timezone

STRING_MAX_LENGTH = 64

class OccupyWardModel(models.Model):
    full_name = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Фамилия И.О.'
    )
    telephone = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Телефон',
        blank=True,
    )
    bed = models.ForeignKey(
        BedModel,
        on_delete=models.CASCADE,
        verbose_name='Койка',
    )
    date_checkin = models.DateField(
        verbose_name='Дата заселения',
        default=timezone.now,
        null=True,
    )
    date_checkout = models.DateField(
        verbose_name='Дата выселения',
        default=timezone.now().date() + timezone.timedelta(days=3),
        null=True,
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )
    operation = models.BooleanField(
        default=False,
        verbose_name='Операция'
    )
    color = RGBColorField(
        default='#8B0000',
        verbose_name='Цвет заливки',
        help_text='Выберите цвет заливки для пациента'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        editable=False,
    )

    def generate_random_char(self):
        return random.choice(string.ascii_letters)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(f"{self.full_name}-{self.bed.number}-{self.date_checkin}"))
            self.slug = base_slug
            while OccupyWardModel.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{self.generate_random_char()}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.full_name} занял койку: {self.bed.number}'

    class Meta:
        verbose_name = 'Заселенная койка'
        verbose_name_plural = 'Заселенные койки'