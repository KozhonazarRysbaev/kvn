from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'get_full_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'sex', 'date_birth', 'avatar', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
