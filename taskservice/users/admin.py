from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import AdminPasswordChangeForm
#
# from tasks.forms import UserChangeForm, UserCreationForm
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


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = ('username', 'last_name', 'first_name', 'is_active')
#     fieldsets = None
#     fields = (
#         'username',
#         ('last_name', 'first_name'),
#         'email', 'password',
#         ('is_superuser', 'is_staff', 'is_active'),
#         ('date_joined', 'last_login'),
#         'groups'
#     )
#     inlines = [
#         WorkerInline,
#         CustomerInline
#     ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'phone', 'is_active']
    list_display_links = list_display[:2]
    # fieldsets = None
    # fields = (
    #         'username',
    #         ('last_name', 'first_name'),
    #         'email', 'password',
    #         ('is_superuser', 'is_staff', 'is_active'),
    #         ('date_joined', 'last_login'),
    #         'groups'
    #     )
    inlines = [
        WorkerInline,
        CustomerInline
    ]
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserCreationForm
#     change_password_form = AdminPasswordChangeForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'phone', 'is_active']
#     list_display_links = list_display[:2]
#     fields = (
#             'username',
#             ('last_name', 'first_name'),
#             'email', 'password',
#             ('is_superuser', 'is_staff', 'is_active'),
#             ('date_joined', 'last_login'),
#             'groups'
#         )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions',)