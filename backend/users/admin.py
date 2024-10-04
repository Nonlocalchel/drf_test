from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
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
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'phone', 'is_active']
    list_display_links = list_display[:2]
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = []
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'phone', 'type', 'photo')}),
        ('Permissions', {'fields': ('groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2', 'type'),
        }),
    )
    inlines = [
        WorkerInline,
        CustomerInline
    ]



