"""
Currency admin
"""

from django.contrib import admin
from .models import PlaidItem

admin.site.register(PlaidItem)
