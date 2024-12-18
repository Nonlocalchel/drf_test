from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import *


class WorkerInline(admin.StackedInline):
    """User worker profile data view on admin panel"""
    verbose_name = "Worker"
    verbose_name_plural = verbose_name
    can_delete = False
    model = Worker


class CustomerInline(admin.StackedInline):
    """User customer profile data view on admin panel"""
    verbose_name = "Customer"
    verbose_name_plural = verbose_name
    can_delete = False
    model = Customer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User view on admin panel"""
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'phone', 'is_active']
    list_display_links = list_display[:2]
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2', 'type'),
        }),
        (_('Personal info'), {'fields': ('email', 'photo')}),
        ('Permissions', {'fields': ('groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')}),
    )

    def get_inline_instances(self, request, obj=None):
        """Hide unnecessary profile data"""
        if obj is None:
            return [CustomerInline(self.model, self.admin_site), WorkerInline(self.model, self.admin_site)]

        if obj.type == User.UserType.CUSTOMER:
            return [CustomerInline(self.model, self.admin_site)]

        return [WorkerInline(self.model, self.admin_site)]
