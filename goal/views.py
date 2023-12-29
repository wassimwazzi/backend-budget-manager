from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import GoalSerializer, GoalContributionSerializer
from .models import Goal, GoalContribution
from queryset_mixin import QuerysetMixin


class GoalView(viewsets.ModelViewSet):
    serializer_class = GoalSerializer

    def get_queryset(self):
        """
        This view should return a list of all the categories
        for the currently authenticated user.
        """
        print("GET QUERYSET")
        user = self.request.user
        queryset = Goal.objects.filter(user=user)
        print(queryset)
        return queryset
        # return self.get_filtered_queryet(queryset)

    def perform_create(self, serializer):
        print("PERFORM CREATE")
        serializer.save(user=self.request.user)
        print("PERFORM CREATE END")

    def create(self, request, *args, **kwargs):
        """
        Create a new goal
        """
        print("CREATE VIEW")
        print(request.data)
        serializer = GoalSerializer(data=request.data, context={"request": request})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print("VALID", serializer.validated_data)
        serializer.save()
        # Create a contribution for the current month

        return Response(serializer.data)
