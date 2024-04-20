from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'last_name', 'first_name', 'middle_name', 'position', 'department')
    search_fields = ('department',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Основная информация о пользователе', {'fields': ('last_name', 'first_name', 'middle_name', 'position', 'department')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
