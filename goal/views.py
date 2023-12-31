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

    def retrieve(self, request, pk=None):
        goal = self.get_object()
        include_overlapping = (
            request.query_params.get("include_overlapping", "").lower() == "true"
        )
        contributions = goal.get_contributions(include_overlapping=include_overlapping)
        context = {"contributions": contributions} if contributions else None
        serializer = GoalSerializer(goal, context=context)
        return Response(serializer.data)
