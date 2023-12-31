from rest_framework import serializers
from .models import Goal, GoalContribution, ContributionRange


class GoalContributionSerializer(serializers.ModelSerializer):
    """
    Goal Contribution serializer
    """

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
        read_only_fields = ("id", "goal", "amount")

    def get_start_date(self, obj):
        return obj.date_range.start_date

    def get_end_date(self, obj):
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
        input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m"
    )
    expected_completion_date = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m"
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)
    contributions = GoalContributionSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super(GoalSerializer, self).to_representation(instance)
        if not "contributions" in self.context:
            return data
        contributions = self.context["contributions"]
        data["contributions"] = GoalContributionSerializer(
            contributions, many=True
        ).data
        return data

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
