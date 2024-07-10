from django.contrib import admin
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
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'phone', 'is_active']
    list_display_links = list_display[:2]
    inlines = [
        WorkerInline,
        CustomerInline
    ]

