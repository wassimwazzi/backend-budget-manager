# Generated by Django 5.0 on 2023-12-30 16:35

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionRange',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'contribution ranges',
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.PositiveIntegerField()),
                ('expected_completion_date', models.DateField()),
                ('actual_completion_date', models.DateField(blank=True, null=True)),
                ('type', models.CharField(choices=[('SAVINGS', 'Savings'), ('DEBT', 'Debt'), ('INVESTMENT', 'Investment')], default='SAVINGS', max_length=20)),
                ('description', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='IN_PROGRESS', max_length=20)),
                ('start_date', models.DateField()),
                ('recurring', models.CharField(choices=[('INDEFINITE', 'Indefinite'), ('FIXED', 'Fixed'), ('NON_RECURRING', 'Non Recurring')], default='NON_RECURRING', max_length=20)),
                ('reccuring_frequency', models.PositiveIntegerField(blank=True, null=True)),
                ('previous_goal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='goal.goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'goals',
            },
        ),
        migrations.CreateModel(
            name='GoalContribution',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percentage', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('date_range', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contributions', to='goal.contributionrange')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='goal.goal')),
            ],
            options={
                'verbose_name_plural': 'goal contributions',
            },
        ),
    ]