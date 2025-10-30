from django.db import models
from django.conf import settings


class ImportFile(models.Model):
    FILE_TYPE_CHOICES = [
        ("students", "Students"),
        ("programs", "Programs"),
        ("courses", "Courses"),
        ("enrollments", "Enrollments"),
        ("results", "Results"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("validated", "Validated"),
        ("error", "Error"),
    ]

    file = models.FileField(upload_to="imports/")
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.file_type})"


class ImportLog(models.Model):
    import_file = models.ForeignKey(
        ImportFile, on_delete=models.CASCADE, related_name="logs"
    )
    message = models.TextField()
    is_error = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'ERROR' if self.is_error else 'INFO'}: {self.message[:50]}"
