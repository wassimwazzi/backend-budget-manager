"""
Insert Currency data
"""

from django.db import migrations


def seed_data(apps, _schema_editor):
    """
    Insert Currency data
    """
    Currency = apps.get_model("currency", "Currency")
    Currency.objects.create(code="CAD")
    Currency.objects.create(code="LBP")
    Currency.objects.create(code="EUR")
    Currency.objects.create(code="USD")
    Currency.objects.create(code="GBP")


class Migration(migrations.Migration):
    """
    Insert Currency data
    """

    dependencies = [
        ("currency", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
