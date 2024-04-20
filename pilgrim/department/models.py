from django.db import models
from django.utils.text import slugify
import random
import string


from unidecode import unidecode

STRING_MAX_LENGTH = 64

class DepartmentModel(models.Model):
    name = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Название отделения',
        unique=True,)
    address = models.CharField(
        max_length=STRING_MAX_LENGTH*2,
        verbose_name='Адрес')
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        editable=False,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'

    def __str__(self):
        return self.name
    
class WardModel(models.Model):
    name = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Наименование палаты',
        )
    department = models.ForeignKey(
        DepartmentModel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Находится в отделении',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        editable=False,)
    
    def generate_random_char(self):
        return random.choice(string.ascii_letters)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(f"pl{self.name} {self.department.name}"))
            self.slug = base_slug
            while WardModel.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{self.generate_random_char()}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Палата'
        verbose_name_plural = 'Палаты'

    def __str__(self):
        return f'Палат №{self.name} "{self.department.name}"'


class BedModel(models.Model):
    number = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Номер койки',
        )
    ward = models.ForeignKey(
        WardModel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Находится в палате',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        editable=False,)

    def generate_random_char(self):
        return random.choice(string.ascii_letters)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(f"{self.number} {self.ward.name} {self.ward.department.name}"))
            self.slug = base_slug
            while BedModel.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{self.generate_random_char()}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Койка'
        verbose_name_plural = 'Койки'

    def __str__(self):
        return f'Койка №{self.number}, палата №{self.ward.name}, {self.ward.department.name}'
