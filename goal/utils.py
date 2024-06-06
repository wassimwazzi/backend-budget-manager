from goal.models import Goal, GoalStatus, GoalRecurranceType
import datetime
import calendar


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def add_months(sourcedate, months):
    """
    Add months to a date
    Handle months with 31 days, 30 days, and February
    """
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def update_status(user=None):
    """
    Update status of all goals
    """
    # get all goals in progress or pending
    goals = Goal.objects.filter(status__in=[GoalStatus.IN_PROGRESS, GoalStatus.PENDING])
    if user:
        goals = goals.filter(user=user)
    for goal in goals:
        if goal.expected_completion_date < datetime.date.today():
            goal.status = (
                GoalStatus.COMPLETED if goal.progress == 100 else GoalStatus.FAILED
            )
            goal.save()
        elif goal.start_date <= datetime.date.today():
            goal.status = GoalStatus.IN_PROGRESS
            goal.save()
        else:
            goal.status = GoalStatus.PENDING
            goal.save()

    return goals


def create_goals(user=None):
    """
    Create new goals for all recurring goals
    """
    # get all goals with recurring set to FIXED OR INDEFINITE
    # AND no goal has it as a previous goal
    goals = Goal.objects.filter(user=user) if user else Goal.objects.all()
    predecessor_goals = goals.values_list("previous_goal__id", flat=True)
    goals = goals.filter(
        recurring__in=[GoalRecurranceType.FIXED, GoalRecurranceType.INDEFINITE],
    )  # .exclude(id__in=predecessor_goals)
    new_goals = []
    for goal in goals:
        if goal.id in predecessor_goals:
            continue
        if (
            diff_month(datetime.date.today(), goal.expected_completion_date)
            <= goal.recurring_frequency - 1
        ):
            continue
        start_date = goal.expected_completion_date + datetime.timedelta(days=1)
        goal_number_of_months = diff_month(
            goal.expected_completion_date, goal.start_date
        )
        # goal_range = goal.expected_completion_date - goal.start_date
        # print(goal_range)
        # add the number of months to the start date
        end_date = add_months(start_date, goal_number_of_months)
        new_goal = Goal.objects.create(
            user=goal.user,
            amount=goal.amount,
            recurring=goal.recurring,
            recurring_frequency=goal.recurring_frequency,
            start_date=start_date,
            expected_completion_date=end_date,
            previous_goal=goal,
            status=GoalStatus.IN_PROGRESS,
            description=goal.description,
        )
        new_goal.save()
        new_goals.append(new_goal)

    return new_goals
