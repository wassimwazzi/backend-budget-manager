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
            "start_date",
            "end_date",
            "goal",
            "percentage",
        )
        read_only_fields = ("id", "end_date", "goal")


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
    contributions = GoalContributionSerializer(many=True)

    def create(self, validated_data):
        print("CREATE")
        print(validated_data)
        contributions = validated_data.pop("contributions")
        print("WWWW")
        print(contributions)
        print(validated_data)
        goal = Goal.objects.create(**validated_data)
        print(goal)
        for contribution in contributions:
            GoalContribution.objects.create(goal=goal, **contribution)
        return goal

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
        read_only_fields = ("id", "user")


# from rest_framework import serializers
# from .models import Goal, GoalContribution


# class GoalSerializer(serializers.ModelSerializer):
#     """
#     Goal serializer
#     """

#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     start_date = serializers.DateField(
#         input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m"
#     )
#     amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)
#     contributions = serializers.PrimaryKeyRelatedField(
#         many=True, read_only=False
#     )

#     class Meta:
#         model = Goal
#         fields = (
#             "id",
#             "amount",
#             "expected_completion_date",
#             "actual_completion_date",
#             "type",
#             "description",
#             "status",
#             "start_date",
#             "recurring",
#             "reccuring_frequency",
#             )
#         read_only_fields = ("id", "user")


# class GoalContributionSerializer(serializers.ModelSerializer):
#     """
#     Goal Contribution serializer
#     """

#     goal = GoalSerializer(read_only=True)

#     class Meta:
#         model = GoalContribution
#         fields = (
#             "id",
#             "amount",
#             "start_date",
#             "end_date",
#             "goal",
#             "percentage",
#         )
#         read_only_fields = ("id", "user", "start_date", "end_date", "goal")
