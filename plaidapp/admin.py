"""
Currency admin
"""

from django.contrib import admin
from .models import PlaidItem, PlaidAccount, PlaidItemSync, PlaidTransaction, Location
from .sync_transactions import sync_transactions


@admin.action(description="Sync selected items")
def sync_item(modeladmin, request, queryset):
    for item in queryset:
        sync_transactions(item.item_id)


@admin.action(description="Delete transactions")
def delete_transactions(modeladmin, request, queryset):
    # delete plaid_transactions where transaction.account.plaid_item is in queryset
    # PlaidTransaction.objects.filter(account__plaid_item__in=queryset).delete()
    for item in queryset:
        accounts = PlaidAccount.objects.filter(item__item_id=item.item_id)
        for account in accounts:
            PlaidTransaction.objects.filter(account=account).delete()
            # account.delete()
        item.last_cursor = None
        PlaidItemSync.objects.filter(item=item).delete()
        item.save()


class PlaidItemAdmin(admin.ModelAdmin):
    actions = [sync_item, delete_transactions]


admin.site.register(PlaidItem, PlaidItemAdmin)
admin.site.register(PlaidAccount)
admin.site.register(PlaidItemSync)
admin.site.register(PlaidTransaction)
admin.site.register(Location)
