"""
Currency admin
"""

from django.contrib import admin
from .models import PlaidItem, PlaidAccount, PlaidItemSync, PlaidTransaction, Location

admin.site.register(PlaidItem)
admin.site.register(PlaidAccount)
admin.site.register(PlaidItemSync)
admin.site.register(PlaidTransaction)
admin.site.register(Location)
