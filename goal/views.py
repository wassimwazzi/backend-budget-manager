from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    GoalSerializer,
    GoalContributionSerializer,
    ContributionRangeSerializer,
)
from .models import Goal, GoalContribution, ContributionRange
from queryset_mixin import QuerysetMixin
import django.core.exceptions


class GoalView(QuerysetMixin, viewsets.ModelViewSet):
    serializer_class = GoalSerializer

    def get_queryset(self):
        """
        This view should return a list of all the categories
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Goal.objects.filter(user=user)
        return self.get_filtered_queryet(queryset)

    def create(self, request):
        serializer = GoalSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except django.core.exceptions.ValidationError as e:
            return Response(e, status=400)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @action(detail=True, methods=["get"])
    def contribution_ranges(self, request, pk=None):
        goal = self.get_object()
        contributions = goal.contribution_ranges
        serializer = ContributionRangeSerializer(contributions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def update_contributions(self, request):
        result = []
        # FIXME: This should be in a transaction
        try:
            for contribution_range in request.data.get("contribution_ranges", []):
                contribution_range_obj = ContributionRange.objects.get(
                    id=contribution_range["id"]
                )
                if not "contributions" in contribution_range:
                    return Response(
                        {"error": "contributions is required for all ranges"},
                        status=400,
                    )
                contributions = contribution_range["contributions"]
                contribution_range_obj.update_contributions(contributions)
                contribution_range_obj.refresh_from_db()
                result.append(contribution_range_obj)
            serializer = ContributionRangeSerializer(result, many=True)
            return Response(serializer.data)
        except django.core.exceptions.ValidationError as e:
            return Response(e, status=400)
