from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "institution", "is_staff", "is_active")
    list_filter = ("institution", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    fieldsets = UserAdmin.fieldsets + (
        ("Institution Info", {"fields": ("institution",)}),
    )
