import calendar
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import rest_framework.serializers as serializers
import django.db.models as models
import csv
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

    def perform_create_or_update(self, serializer):
        self.validate_date()
        user = self.request.user
        category_id = self.request.data.get("category")
        if category_id:
            try:
                category = Category.objects.get(id=category_id, user=user)
            except (Category.DoesNotExist, ValueError) as e:
                raise serializers.ValidationError(
                    "Category not found or does not belong to the user"
                ) from e
            serializer.save(category=category, inferred_category=False)
        else:
            serializer.save()

    def perform_create(self, serializer):
        self.perform_create_or_update(serializer)

    def perform_update(self, serializer):
        self.perform_create_or_update(serializer)

    @action(detail=False, methods=["post"])
    def infer(self, request):
        # webhook_url = request.data.get("webhook_url") or "webhook_url"
        # FIXME: Uncomment to add celery task back
        # task = infer_categories_task.delay(request.user.id)
        # result = task.get()
        result = infer_categories_task(request.user.id)
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
                .annotate(total=models.Sum("amount"))
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
            .annotate(total=models.Sum("amount"))
            .values("category__category", "total")
            .annotate(category=models.F("category__category"))
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
            .annotate(total=models.Sum("amount"))
            .order_by("-date__year", "-date__month")
        )

        income_by_month = (
            queryset.filter(category__income=True)
            .values("date__year", "date__month")
            .annotate(total=models.Sum("amount"))
            .order_by("-date__year", "-date__month")
        )

        # Get unique months from spend_by_month and income_by_month
        months = {
            (month["date__year"], month["date__month"]) for month in spend_by_month
        }.union(
            {(month["date__year"], month["date__month"]) for month in income_by_month}
        )
        # sort months by year and month
        months = sorted(months, key=lambda x: (x[0], x[1]), reverse=True)

        response_data = []
        for month in months:
            spend = next(
                (
                    month_spend["total"]
                    for month_spend in spend_by_month
                    if month_spend["date__year"] == month[0]
                    and month_spend["date__month"] == month[1]
                ),
                0,
            )
            income = next(
                (
                    month_income["total"]
                    for month_income in income_by_month
                    if month_income["date__year"] == month[0]
                    and month_income["date__month"] == month[1]
                ),
                0,
            )
            response_data.append(
                {
                    "month": f"{month[0]}-{month[1]:02d}",
                    "spend": spend,
                    "income": income,
                }
            )

        return Response(response_data, status=200)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        # Over all transactions history, get average spend and income by month
        # Formula: average_spend = total_spend / number_of_months
        queryset = self.get_queryset()
        unique_months = queryset.dates("date", "month")
        totals = (
            queryset.values("category__income")
            .annotate(total_amount=models.Sum("amount"), count=models.Count("id"))
            .order_by("-category__income")
        )
        # NOTE: Use count if needed lateravg_income = (
        total_income = totals.filter(category__income=True).first()
        total_spend = totals.filter(category__income=False).first()
        response = {
            "monthly_average": {
                "income": (
                    total_income["total_amount"] / len(unique_months)
                    if total_income
                    else 0
                ),
                "spend": (
                    total_spend["total_amount"] / len(unique_months)
                    if total_spend
                    else 0
                ),
            }
        }

        month = request.query_params.get("month")
        if month:
            # show total spend and income for the month, as well as last month
            try:
                month = timezone.datetime.strptime(month, "%Y-%m").date()
            except ValueError as e:
                raise serializers.ValidationError(
                    f"Invalid month format: {month}, must be YYYY-MM"
                ) from e
            month_start = month.replace(day=1)
            month_end = month.replace(
                day=calendar.monthrange(month.year, month.month)[1]
            )
            last_month_start = month_start - timezone.timedelta(days=1)
            last_month_start = last_month_start.replace(day=1)
            last_month_end = month_start - timezone.timedelta(days=1)
            this_month_totals = (
                queryset.filter(date__range=(month_start, month_end))
                .values("category__income")
                .annotate(total_amount=models.Sum("amount"))
                .order_by("-category__income")
            )
            last_month_totals = (
                queryset.filter(date__range=(last_month_start, last_month_end))
                .values("category__income")
                .annotate(total_amount=models.Sum("amount"))
                .order_by("-category__income")
            )
            this_month_income = this_month_totals.filter(category__income=True).first()
            this_month_spend = this_month_totals.filter(category__income=False).first()
            response["this_month"] = {
                "income": this_month_income["total_amount"] if this_month_income else 0,
                "spend": this_month_spend["total_amount"] if this_month_spend else 0,
            }
            last_month_income = last_month_totals.filter(category__income=True).first()
            last_month_spend = last_month_totals.filter(category__income=False).first()
            response["last_month"] = {
                "income": last_month_income["total_amount"] if last_month_income else 0,
                "spend": last_month_spend["total_amount"] if last_month_spend else 0,
            }

        return Response(response, status=200)

    @action(detail=False, methods=["get"])
    def balance(self, request):
        queryset = self.get_queryset()
        # if transaction's category is income, add amount to balance
        # if transaction's category is spend, subtract amount from balance
        balance = queryset.aggregate(
            balance=models.Sum(
                models.Case(
                    models.When(category__income=True, then=models.F("amount")),
                    default=-models.F("amount"),
                    output_field=models.DecimalField(),
                )
            )
        )
        if balance["balance"] is None:
            balance["balance"] = 0
        return Response(balance, status=200)

class ExportTransactionsViewSet(QuerysetMixin, APIView):

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Transaction.objects.filter(user=user)
        return self.get_filtered_queryet(queryset)

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="transactions.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "code",
                "amount",
                "currency",
                "date",
                "description",
                "category",
                "inferred_category",
            ]
        )
        transactions = self.get_queryset()
        for transaction in transactions:
            writer.writerow(
                [
                    transaction.code,
                    transaction.amount,
                    transaction.currency.code,
                    transaction.date,
                    transaction.description,
                    transaction.category.category,
                    transaction.inferred_category,
                ]
            )
        return response