from rest_framework import serializers
from django.db import models
import django.core.exceptions


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


class Filter:
    """
    A class to represent a filter
    """

    VALID_OPERATORS = [
        "exact",
        "iexact",
        "contains",
        "icontains",
        "startswith",
        "istartswith",
        "endswith",
        "iendswith",
        "gt",
        "gte",
        "lt",
        "lte",
    ]

    def __init__(self, filter_field, filter_value, filter_operator="exact"):
        self.filter_field = filter_field
        self.filter_value = filter_value
        filter_operator = filter_operator.lower()
        self.filter_operator = (
            filter_operator if filter_operator in self.VALID_OPERATORS else "exact"
        )

    def as_dict(self):
        """
        Return the filter as a dictionary that can be passed to the filter method of a queryset
        """
        return {f"{self.filter_field}__{self.filter_operator}": self.filter_value}

    def apply_filter(self, queryset):
        """
        Apply the filter to the queryset
        """
        return queryset.filter(**self.as_dict())


class FilterList:
    """
    A class to represent a list of filters
    """

    def __init__(self, filter_fields, filter_values, filter_operators):
        if len(filter_fields) != len(filter_values) or len(filter_fields) != len(
            filter_operators
        ):
            raise serializers.ValidationError(
                "filter_fields, filter_values, and filter_operators must have the same length"
            )
        self.filters = [
            Filter(filter_field, filter_value, filter_operator)
            for filter_field, filter_value, filter_operator in zip(
                filter_fields, filter_values, filter_operators
            )
        ]

    def apply_filters(self, queryset):
        """
        Apply filters to the queryset
        """
        filters = {}
        for f in self.filters:
            filters.update(f.as_dict())
        return queryset.filter(**filters)

    def apply_filters_or(self, queryset):
        """
        Apply filters to the queryset using OR
        """
        filters = models.Q()
        for f in self.filters:
            filters |= models.Q(**f.as_dict())
        return queryset.filter(filters)


class QuerysetMixin:
    """
    Mixin for filtering and sorting querysets
    Pass a filter field mapping to map filter fields to related fields
    TODO: Allow more complex queries with OR and AND operators like LDAP
    """

    def get_filter_list(self, filter_fieds_mapping=None):
        """
        Get filter list from query string parameters
        Map filter fields to related fields if necessary
        """
        filter_fields = self.request.query_params.getlist("filter[]", [])
        filter_values = self.request.query_params.getlist("filter_value[]", [])
        filter_operators = self.request.query_params.getlist("filter_operator[]", [])

        if filter_fieds_mapping:
            filter_fields = [
                filter_fieds_mapping.get(filter_field, filter_field)
                for filter_field in filter_fields
            ]
        return FilterList(filter_fields, filter_values, filter_operators)

    def get_sort_params(self, fields_mapping=None):
        """
        Get sort field and order from query string parameters
        """
        sort_field = self.request.query_params.get("sort", None)
        sort_order = self.request.query_params.get("order", None)
        if not sort_field or not sort_order:
            return None, None
        sort_order = sort_order.lower()
        if sort_order not in ["asc", "desc"]:
            raise serializers.ValidationError("Invalid sort order, must be asc or desc")
        if fields_mapping:
            sort_field = fields_mapping.get(sort_field, sort_field)
        sort_order = "" if sort_order == "asc" else "-"
        return sort_field, sort_order

    def get_filtered_queryet(self, queryset, fields_mapping=None):
        """
        Filters and sort the queryset based on query string parameters
        """
        filter_list: FilterList = self.get_filter_list(fields_mapping)
        try:
            queryset = filter_list.apply_filters(queryset)
        except Exception as e:
            raise serializers.ValidationError(e)

        # Sort by a single field
        sort_field, sort_order = self.get_sort_params(fields_mapping)

        if sort_field and sort_order:
            # prevent duplicates in pagination https://stackoverflow.com/questions/5044464/django-pagination-is-repeating-results
            try:
                queryset = queryset.order_by(f"{sort_order}{sort_field}", "id")
            except django.core.exceptions.FieldError as exc:
                raise serializers.ValidationError("Invalid sort field") from exc

        return queryset
