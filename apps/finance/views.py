from apps.finance.models import Transaction
from apps.finance.forms import TransactionForm

from apps.shared.utils import dates_contants

from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('finance:list')


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 25

    def get_queryset(self):
        today = datetime.today()
        month_param = today.month
        year_param = today.year
        params = self.request.GET
        if filter_month := params.get('month'):
            month_param = filter_month
        if filter_year := params.get('year'):
            year_param = filter_year
        qs = super().get_queryset().filter(
            due_date__month=month_param,
            due_date__year=year_param,
        )
        if q := params.get('q'):
            qs = qs.filter(title__icontains=q)
        if date := params.get('date'):
            qs = qs.filter(due_date=date)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = dates_contants.YEARS
        context['months'] = dates_contants.MONTHS_MAPPING
        context = context | Transaction.services.get_transaction_context(qs=self.get_queryset())
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        context["querystring"] = query_params.urlencode()
        return context


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('finance:list')


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('finance:list')


class TransactionToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.toggle_paid()

        referer = request.META.get("HTTP_REFERER")
        if referer:
            return redirect(referer)

        return redirect('finance:list')
