from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User

from .models import Usuario

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    form = UserChangeForm
    add_form = UserCreationForm


# Deixar campos como leitura
@admin.register(Usuario)
class UsarioAdmin(admin.ModelAdmin):
    readonly_fields = ('nome', 'email', 'senha')