from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BudgetSerializer
from .models import Budget
from category.models import Category
import datetime
import rest_framework.serializers as serializers
from queryset_mixin import QuerysetMixin


FILTER_FIELDS_MAPPING = {
    "category": "category__category",
}


class BudgetView(QuerysetMixin, viewsets.ModelViewSet):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        """
        This view should return a list of all the budgets
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Budget.objects.filter(user=user)

        return self.get_filtered_queryet(queryset, FILTER_FIELDS_MAPPING)

    def perform_create_or_update(self, serializer, is_create=False):
        user = self.request.user
        validated_data = serializer.validated_data

        category_id = self.request.data.get("category")
        start_date = validated_data.get("start_date")
        if category_id:
            try:
                category = Category.objects.get(id=category_id, user=user)
            except (Category.DoesNotExist, ValueError) as e:
                raise serializers.ValidationError(
                    "Category not found or does not belong to the user"
                ) from e
            if (
                is_create
                and Budget.objects.filter(
                    category=category, user=user, start_date=start_date
                ).exists()
            ):
                raise serializers.ValidationError(
                    "Budget for this category and date already exists"
                )
            serializer.save(category=category)
        else:
            serializer.save()

    def perform_create(self, serializer):
        self.perform_create_or_update(serializer, is_create=True)

    def perform_update(self, serializer):
        self.perform_create_or_update(serializer)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        month = request.query_params.get("month")
        if not month:
            return Response({"error": "month param is required"}, status=400)
        try:
            month = datetime.datetime.strptime(month, "%Y-%m").date()
        except ValueError:
            return Response({"error": "month must be in YYYY-MM format"}, status=400)
        budget_summary = Budget.get_budget_by_category(month, request.user)
        return Response(budget_summary, status=200)
