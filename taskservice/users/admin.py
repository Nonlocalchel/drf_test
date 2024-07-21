from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class WorkerInline(admin.StackedInline):
    verbose_name = "Worker"
    verbose_name_plural = verbose_name
    can_delete = False
    model = Worker


class CustomerInline(admin.StackedInline):
    verbose_name = "Consumer"
    verbose_name_plural = verbose_name
    can_delete = False
    model = Customer


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'is_active')
    fieldsets = None
    fields = (
        'username',
        ('last_name', 'first_name'),
        'email', 'password',
        ('is_superuser', 'is_staff', 'is_active'),
        ('date_joined', 'last_login'),
        'groups'
    )
    inlines = [
        WorkerInline,
        CustomerInline
    ]

