from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    institution = models.ForeignKey(
        "core.Institution", on_delete=models.SET_NULL, null=True, blank=True
    )
    role = models.CharField(max_length=50, default="staff")

    def __str__(self):
        return (
            f"{self.username} ({self.institution})"
            if self.institution
            else self.username
        )
