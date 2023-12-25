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
    # generate unique hash for filename
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    print(now)
    try:
        filename, extension = filename.split(".")
    except ValueError as e:
        raise ValueError(f"Invalid filename: {filename}") from e
    return f"uploads/user-{user.id}/{filename}_{now}.{extension}"


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
    message = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Validate extension before saving.
        """
        if self.file.name and not self.file.name.endswith(".csv"):
            raise Exception("Invalid file extension.")
        if len(self.message) > 500:
            self.message = self.message[:497] + "..."
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete file from disk when deleting the object.
        """
        self.file.delete()
        super().delete(*args, **kwargs)
