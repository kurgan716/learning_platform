# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ['username', 'email', 'role', 'first_name', 
                   'last_name', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('role', 'bio', 'profile_picture', 'date_of_birth')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('role', 'bio', 'profile_picture', 'date_of_birth')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)