from django.db import models
from django.db.models import Sum


def get_total_sum(qs):
    return qs.aggregate(total=Sum('value'))['total'] or 0


class TransactionManager(models.Manager):

    def get_transaction_context(self, qs):
        context = {}
        income_transactions = qs.filter(transaction_type='income')
        outcome_transactions = qs.filter(transaction_type='outcome')
        context['total_in'] = round(get_total_sum(income_transactions), 2)
        context['total_out'] = round(get_total_sum(outcome_transactions) or 0, 2)
        context['total_pending'] = round(get_total_sum(
            outcome_transactions.filter(is_paid=False)
        ), 2)
        context['balance'] = context['total_in'] - context['total_out']
        return context
