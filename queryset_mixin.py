from rest_framework import serializers
from django.db import models


def find_related_field(model, field_name, visited_models=None, depth=0, link_name=""):
    # Initialize the set of visited models to avoid infinite loops
    if visited_models is None:
        visited_models = set()

    # Add the current model to the set of visited models
    visited_models.add(model)

    # Iterate through the model's fields and relationships
    for field in model._meta.get_fields():
        # Check if the field is a ForeignKey or OneToOneField
        # Check if the related field's name matches the given field_name
        if field.name == field_name:
            return True, depth, f"{link_name}{field.name}"
        if isinstance(field, (models.ForeignKey, models.OneToOneField)):
            # Check if the related model has already been visited
            if field.related_model not in visited_models:
                # Recursively check the related model with increased depth
                result, related_depth, link_name = find_related_field(
                    field.related_model,
                    field_name,
                    visited_models,
                    depth + 1,
                    f"{link_name}{field.name}__",
                )
                if result:
                    return result, related_depth, link_name

    # If no matching field is found, return False and depth as -1
    return False, -1, ""


class QuerysetMixin:
    def get_filtered_queryet(self, queryset, filter_callback=None):
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
            ):  # FIXME: front-end sends category instead of category__category. Fix is actually in front-end
                filter_field = "category__category"
            if filter_callback:
                filter_field_query = filter_callback(filter_field)
            else:
                filter_field_query = f"{filter_field}__icontains"
            filters[filter_field_query] = filter_value

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
                f"{'' if sort_order == 'asc' else '-'}{sort_field}", 'id' # prevent duplicates in pagination https://stackoverflow.com/questions/5044464/django-pagination-is-repeating-results
            )

        return queryset
