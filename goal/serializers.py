from rest_framework import serializers
from .models import Goal, GoalContribution


class GoalContributionSerializer(serializers.ModelSerializer):
    """
    Goal Contribution serializer
    """

    class Meta:
        model = GoalContribution
        fields = (
            "id",
            "amount",
            "goal",
            "percentage",
        )
        read_only_fields = ("id", "goal", "amount")


class GoalSerializer(serializers.ModelSerializer):
    """
    Goal serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    start_date = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m"
    )
    expected_completion_date = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m"
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)
    contributions = GoalContributionSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = (
            "id",
            "amount",
            "expected_completion_date",
            "actual_completion_date",
            "type",
            "description",
            "status",
            "start_date",
            "recurring",
            "reccuring_frequency",
            "contributions",
            "user",
        )
        read_only_fields = ("id", "user", "contributions")
