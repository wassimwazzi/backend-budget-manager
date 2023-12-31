from django.contrib import admin
from .models import Goal, GoalContribution, ContributionRange

admin.site.register(Goal)
admin.site.register(GoalContribution)
admin.site.register(ContributionRange)
