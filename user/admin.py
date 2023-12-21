from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'email_verify','password')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined', 'date_sent_mail')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'email_verify', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_sent_mail', )
    list_display = ('username', 'email', 'email_verify')
    search_fields = ('email', )
    ordering = ('email',)
   
 
admin.site.register(User, CustomUserAdmin)
