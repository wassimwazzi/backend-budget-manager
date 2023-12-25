from rest_framework import serializers
from .models import FileUpload


class CustomFileField(serializers.FileField):
    """
    Custom FileField serializer to customize file serialization
    """

    def to_representation(self, value):
        filename, extension = value.name.split("/")[-1].split(".")
        filename = filename.split("_")
        # join all but last element of filename
        filename = "_".join(filename[:-1])
        return f"{filename}.{extension}"


class FileUploadSerializer(serializers.ModelSerializer):
    """
    FileUpload serializer with custom file serialization
    """

    file = CustomFileField()

    class Meta:
        model = FileUpload
        fields = ("id", "file", "date", "status", "message", "user")
        read_only_fields = ("id", "user", "status", "message", "date")

    def validate_file(self, value):
        """
        Validate file
        """
        if value.name and not value.name.endswith(".csv"):
            raise serializers.ValidationError("Invalid file extension.")
        return value
