from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import DepartmentModel, WardModel, BedModel
from django.contrib.auth.models import Group

class DepartmenAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'slug',
        )
    
class WardAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'department',
        'slug',
        )
    
class BedAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'ward',
        'slug',
        )


admin.site.register(WardModel, WardAdmin)
admin.site.register(BedModel, BedAdmin)
admin.site.register(DepartmentModel, DepartmenAdmin)
admin.site.unregister(Group)