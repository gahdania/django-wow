from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Account
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'display_name', 'battle_tag', 'is_staff', 'preferred_locale')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Display', {'fields': ('display_name', 'battle_tag', 'region', 'preferred_locale')}),
        ('Flags', {'fields': ('is_active', 'is_staff')})
    )
    add_fieldsets = (
        (None, {
            'class': ('wide',),
            'fields': ('username', 'display_name', 'email', 'password1', 'password2', 'battle_tag',
                       'region', 'preferred_locale'),
        }),
    )

    search_fields = ('email', 'display_name', 'username')
    ordering = ('username', 'email')
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(Account)
