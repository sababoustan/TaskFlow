from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_superuser', 'is_active',
                    'is_verified')
    list_filter = ('is_superuser', 'is_active', 'is_staff', 'is_verified')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    fieldsets = (
        ('Authentication', {
            "fields": (
                'email', 'password'
            ),
        }),
        ("Personal Info", {
            "fields": ("full_name",),
        }),
        ('Permissions', {
            "fields": (
                'is_staff', 'is_active', 'is_superuser', 'is_verified'
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2',
                       'is_staff', 'is_active', 'is_superuser',),
            }),
    )


admin.site.register(User, CustomUserAdmin)