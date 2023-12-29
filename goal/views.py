from rest_framework import viewsets
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
        data = request.data.copy()
        if not request.data.get("contributions"):
            data["contributions"] = []
        serializer = GoalSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except django.core.exceptions.ValidationError as e:
            return Response(e, status=400)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
