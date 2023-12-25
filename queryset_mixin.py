from rest_framework import serializers


class QuerysetMixin:
    def get_filtered_queryet(self, queryset):
        """
        Filters and sort the queryset based on query string parameters
        """
        model_class = queryset.model
        filters = {}
        # Get filter parameters from query string
        filter_fields = self.request.query_params.getlist("filter[]", [])
        filter_values = self.request.query_params.getlist("filter_value[]", [])

        # Validate filter fields
        valid_fields = [f.name for f in model_class._meta.get_fields()]
        for filter_field in filter_fields:
            if filter_field not in valid_fields:
                raise serializers.ValidationError(
                    f"Invalid filter field: {filter_field}"
                )

        # Apply filters
        for filter_field, filter_value in zip(filter_fields, filter_values):
            if (
                filter_field == "category" and model_class.__name__ != "Category"
            ):  # FIXME
                filter_field = "category__category"
            filters[f"{filter_field}__icontains"] = filter_value

        queryset = queryset.filter(**filters)

        # Sort by a single field
        sort_field = self.request.query_params.get("sort", None)
        sort_order = self.request.query_params.get("order", None)

        if sort_field and sort_order:
            if sort_field not in valid_fields:
                raise serializers.ValidationError("Invalid sort field")

            if sort_field == "category" and model_class.__name__ != "Category":  # FIXME
                sort_field = "category__category"

            if sort_order not in ["asc", "desc"]:
                raise serializers.ValidationError(
                    "Invalid sort order, must be asc or desc"
                )

            queryset = queryset.order_by(
                f"{'' if sort_order == 'asc' else '-'}{sort_field}"
            )

        return queryset
