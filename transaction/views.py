from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import rest_framework.serializers as serializers
from .serializers import TransactionSerializer
from .models import Transaction
from category.models import Category
from django.utils import timezone
from .tasks import infer_categories_task


class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

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
            if filter_field not in [f.name for f in Transaction._meta.get_fields()]:
                raise serializers.ValidationError("Invalid filter")
            if filter_field == "category":
                filter_field = "category__category"
            queryset = Transaction.objects.filter(
                user=user, **{f"{filter_field}__icontains": filter_value}
            )
        else:
            queryset = Transaction.objects.filter(user=user)
        sort_field = self.request.query_params.get("sort", None)
        sort_order = self.request.query_params.get("order", None)
        if sort_field and sort_order:
            if sort_field not in [f.name for f in Transaction._meta.get_fields()]:
                raise serializers.ValidationError("Invalid sort field")
            if sort_field == "category":
                sort_field = "category__category"
            if sort_order not in ["asc", "desc"]:
                raise serializers.ValidationError(
                    "Invalid sort order, must be asc or desc"
                )
            queryset = queryset.order_by(
                f"{'' if sort_order == 'asc' else '-'}{sort_field}"
            )
        return queryset

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
        task = infer_categories_task.delay(request.user.id)
        result = task.get()
        if result:
            return Response({"message": "Inference completed"}, status=200)
        return Response({"message": "Inference failed"}, status=500)
