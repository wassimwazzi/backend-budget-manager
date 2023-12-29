from rest_framework import viewsets, serializers
from rest_framework.response import Response
from .serializers import GoalSerializer, GoalContributionSerializer
from .models import Goal, GoalContribution
from queryset_mixin import QuerysetMixin
import django.core.exceptions


class GoalView(QuerysetMixin, viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    http_method_names = ["get", "post", "patch", "delete"]

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

    def partial_update(self, request, *args, **kwargs):
        if request.data.get("contributions"):
            raise serializers.ValidationError(
                "Contributions cannot be updated from here"
            )
        return super().partial_update(request, *args, **kwargs)
