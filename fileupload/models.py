"""
File Upload Model
"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Status(models.TextChoices):
    """
    Status
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


def upload_to(instance, filename):
    user = instance.user
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename, extension = filename.split(".")
    return f"uploads/user-{user.id}/{filename}-{now}.{extension}"


class FileUpload(models.Model):
    """
    Upload a file to be processed.
    """

    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=upload_to)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    message = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
