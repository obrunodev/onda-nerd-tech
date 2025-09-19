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

    def filter_transactions(self, qs, params):
        day_param = None
        month_param = None
        year_param = None

        if filter_day := params.get('day'):
            day_param = filter_day
        if filter_month := params.get('month'):
            month_param = filter_month
        if filter_year := params.get('year'):
            year_param = filter_year

        if day_param:
            qs = qs.filter(due_date__day=day_param)
        if month_param:
            qs = qs.filter(due_date__month=month_param)
        if year_param:
            qs = qs.filter(due_date__year=year_param)

        if q := params.get('q'):
            qs = qs.filter(title__icontains=q)
        if date := params.get('date'):
            qs = qs.filter(due_date=date)

        return qs
