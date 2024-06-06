from rest_framework import serializers
from .models import Goal, GoalContribution, ContributionRange, GoalRecurranceType


class GoalSmallSerializer(serializers.ModelSerializer):
    """
    Goal serializer
    """

    class Meta:
        model = Goal
        fields = (
            "id",
            "description",
            "status",
            "is_finalized",
        )
        read_only_fields = ("id",)


class GoalContributionSerializer(serializers.ModelSerializer):
    """
    Goal Contribution serializer
    """

    goal = GoalSmallSerializer(read_only=True)
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = GoalContribution
        fields = (
            "id",
            "amount",
            "goal",
            "start_date",
            "end_date",
            "percentage",
        )
        read_only_fields = ("id", "goal", "amount", "start_date", "end_date")

    def get_start_date(self, obj):
        if not hasattr(obj, "date_range"):
            return None
        return obj.date_range.start_date

    def get_end_date(self, obj):
        if not hasattr(obj, "date_range"):
            return None
        return obj.date_range.end_date


class ContributionRangeSerializer(serializers.ModelSerializer):
    """
    Contribution Range serializer
    """

    contributions = GoalContributionSerializer(many=True, read_only=True)

    class Meta:
        model = ContributionRange
        fields = ("id", "start_date", "end_date", "user", "contributions")
        read_only_fields = ("id", "user", "contributions")


class GoalSerializer(serializers.ModelSerializer):
    """
    Goal serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    start_date = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m-%d"
    )
    expected_completion_date = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m-%d"
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
            "progress",
            "total_contributed",
            "type",
            "description",
            "status",
            "start_date",
            "recurring",
            "recurring_frequency",
            "contributions",
            "user",
        )
        read_only_fields = ("id", "user", "contributions")
