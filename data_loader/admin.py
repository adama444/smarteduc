from django.contrib import admin
from .models import ImportFile, ImportLog


@admin.register(ImportFile)
class ImportFileAdmin(admin.ModelAdmin):
    list_display = ("file", "file_type", "status", "uploaded_by", "uploaded_at")
    list_filter = ("file_type", "status")
    search_fields = ("file", "uploaded_by__username")


@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    list_display = ("import_file", "is_error", "message", "created_at")
    list_filter = ("is_error",)
