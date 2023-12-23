from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
import rest_framework.serializers as serializers
from django.conf import settings
from .serializers import FileUploadSerializer
from .models import FileUpload
from .tasks import process_file
import os


class FileUploadView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FileUploadSerializer

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        user = self.request.user
        filter_field = self.request.query_params.get("filter", None)
        filter_value = self.request.query_params.get("filter_value", None)
        if filter_field and filter_value:
            # validate filter is a valid field
            if filter_field not in [f.name for f in FileUpload._meta.get_fields()]:
                raise serializers.ValidationError("Invalid filter")
            queryset = FileUpload.objects.filter(
                user=user, **{f"{filter_field}__icontains": filter_value}
            )
        else:
            queryset = FileUpload.objects.filter(user=user)
        sort_field = self.request.query_params.get("sort", None)
        sort_order = self.request.query_params.get("order", None)
        if sort_field and sort_order:
            if sort_field not in [f.name for f in FileUpload._meta.get_fields()]:
                raise serializers.ValidationError("Invalid sort field")
            if sort_order not in ["asc", "desc"]:
                raise serializers.ValidationError(
                    "Invalid sort order, must be asc or desc"
                )
            queryset = queryset.order_by(
                f"{'' if sort_order == 'asc' else '-'}{sort_field}"
            )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_upload = serializer.save(user=self.request.user)
        task = process_file.delay(file_upload.id)
        result = task.get()
        if not result:
            return Response(
                "Failed to process file", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        # Return the number of deleted transactions
        instance = self.get_object()
        transaction_count = instance.transaction_set.count()
        self.perform_destroy(instance)
        return Response(
            {"transaction_count": transaction_count}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def template(self, request, *args, **kwargs):
        file_path = "templates/template.csv"
        file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        with open(file_full_path, "r", encoding="utf-8") as f:
            file_data = f.read()
        return Response(file_data, status=status.HTTP_200_OK)
