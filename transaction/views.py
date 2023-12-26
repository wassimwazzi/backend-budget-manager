from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import rest_framework.serializers as serializers
from django.db.models import Sum, F
from .serializers import TransactionSerializer
from .models import Transaction
from category.models import Category
from django.utils import timezone
from .tasks import infer_categories_task
from queryset_mixin import QuerysetMixin


class TransactionView(QuerysetMixin, viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Transaction.objects.filter(user=user)
        return self.get_filtered_queryet(queryset)

    def validate_date(self):
        date = self.request.data.get("date")
        if not date:
            return
        date = timezone.datetime.strptime(date, "%Y-%m-%d").date()
        if date > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future")

    def perform_create(self, serializer):
        self.validate_date()
        category = self.request.data.get("category")
        try:
            category = Category.objects.get(id=category)
        except (Category.DoesNotExist, ValueError) as e:
            raise serializers.ValidationError("Category not found: {}".format(e))
        serializer.save(
            user=self.request.user, category=category, inferred_category=False
        )

    def perform_update(self, serializer):
        self.validate_date()
        category_id = self.request.data.get("category")
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except (Category.DoesNotExist, ValueError) as e:
                raise serializers.ValidationError("Category not found: {}".format(e))
            serializer.save(category=category, inferred_category=False)
        else:
            serializer.save(inferred_category=False)

    @action(detail=False, methods=["post"])
    def infer(self, request):
        # webhook_url = request.data.get("webhook_url") or "webhook_url"
        task = infer_categories_task(request.user.id)
        result = task(blocking=True)
        if result:
            return Response({"message": "Inference completed"}, status=200)
        return Response({"message": "Inference failed"}, status=500)

    @action(detail=False, methods=["get"])
    def spend_by_category(self, request):
        queryset = self.get_queryset()
        monthly = request.query_params.get("monthly", False)
        if monthly:
            # get total spend by category by month
            spend_by_category = (
                queryset.filter(category__income=False)
                .values("category__category", "date__year", "date__month")
                .annotate(total=Sum("amount"))
                .order_by("-date__year", "-date__month")
            )
            response_data = [
                {
                    "category": category["category__category"],
                    "month": f"{category['date__year']}-{category['date__month']:02d}",
                    "total": category["total"],
                }
                for category in spend_by_category
            ]
            return Response(response_data, status=200)
        # get total spend by category
        spend_by_category = (
            queryset.filter(category__income=False)
            .values("category__category")
            .annotate(total=Sum("amount"))
            .values("category__category", "total")
            .annotate(category=F("category__category"))
            .values("category", "total")
            .order_by("-total")
        )
        return Response(spend_by_category, status=200)

    @action(detail=False, methods=["get"])
    def spend_vs_income_by_month(self, request):
        # For each month, get total spend and total income
        queryset = self.get_queryset()
        spend_by_month = (
            queryset.filter(category__income=False)
            .values("date__year", "date__month")
            .annotate(total=Sum("amount"))
            .order_by("-date__year", "-date__month")
        )

        income_by_month = (
            queryset.filter(category__income=True)
            .values("date__year", "date__month")
            .annotate(total=Sum("amount"))
            .order_by("-date__year", "-date__month")
        )

        # Combine spend and income by month
        response_data = [
            {
                "month": f"{month['date__year']}-{month['date__month']:02d}",
                "spend": month["total"] if month["total"] is not None else 0,
                "income": next(
                    (
                        income["total"]
                        for income in income_by_month
                        if income["date__year"] == month["date__year"]
                        and income["date__month"] == month["date__month"]
                    ),
                    0,
                ),
            }
            for month in spend_by_month
        ]

        return Response(response_data, status=200)
