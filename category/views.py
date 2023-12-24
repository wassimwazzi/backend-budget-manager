from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import CategorySerializer
from .models import Category
from queryset_mixin import QuerysetMixin


class CategoryView(QuerysetMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        This view should return a list of all the categories
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Category.objects.filter(user=user)
        return self.get_filtered_queryet(queryset)

    def list(self, request):
        queryset = self.get_queryset()
        paginate = self.request.query_params.get("paginate", None)
        # If paginate is false, return all categories
        if paginate == "false":
            serializer = CategorySerializer(queryset, many=True)
            return Response(serializer.data)
        # If paginate is true, return paginated categories
        page = self.paginate_queryset(queryset)
        serializer = CategorySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
