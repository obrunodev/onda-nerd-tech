from apps.finance.models import Transaction

from django.contrib import admin


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    ...
