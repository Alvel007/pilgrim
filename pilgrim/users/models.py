from django.contrib.auth.models import AbstractUser
from django.db import models

from department.models import DepartmentModel

STRING_MAX_LENGTH = 64

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=STRING_MAX_LENGTH,
        unique=True,
        verbose_name="Логин"
    )
    first_name = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Фамилия'
    )
    middle_name = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Отчество'
    )
    position = models.CharField(
        max_length=STRING_MAX_LENGTH,
        verbose_name='Должность'
    )
    department = models.ForeignKey(
        DepartmentModel,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='Работает в отделении',
    )

    def __str__(self):
        first_initial = self.first_name[0] if self.first_name else ''
        middle_initial = self.middle_name[0] if self.middle_name else ''
        return f'{self.last_name} {first_initial}.{middle_initial}.'