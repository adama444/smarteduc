from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    institution = models.ForeignKey(
        "core.Institution", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return (
            f"{self.username} ({self.institution})"
            if self.institution
            else self.username
        )
