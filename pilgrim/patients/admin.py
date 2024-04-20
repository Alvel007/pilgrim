from django.contrib import admin
from .models import OccupyWardModel


class OccupyWardAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'telephone',
        'bed',
        'date_checkin',
        'date_checkout',
        'operation',
        'color']
    list_filter = [
        'bed',
        'operation']
    search_fields = [
        'full_name',
        'telephone',
        'comment']
    readonly_fields = ['slug',]

admin.site.register(OccupyWardModel, OccupyWardAdmin)