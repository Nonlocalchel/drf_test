from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('customer',)
    list_display = ['id', 'title', 'time_create', 'status', 'customer', 'worker', 'report', 'time_close']
    list_display_links = list_display[:2]

