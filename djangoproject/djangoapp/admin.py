# djangoapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff", "is_active"]


# Register your CustomUser model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
