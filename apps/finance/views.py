from apps.finance.models import Transaction
from apps.finance.forms import TransactionForm

from apps.shared.utils import dates_contants

from datetime import timedelta

from dateutil.relativedelta import relativedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('finance:list')

    def form_valid(self, form):
        installments_quantity = form.cleaned_data.get('installments_quantity', 1)
        original_title = form.cleaned_data['title']
        original_value = form.cleaned_data['value']
        original_due_date = form.cleaned_data['due_date']

        transactions_to_create = []

        if installments_quantity <= 1:
            transaction = form.save(commit=False)
            transactions_to_create.append(transaction)

        else:
            installment_value = original_value / installments_quantity

            parent_transaction = form.save(commit=False)
            parent_transaction.title = f'{original_title} (1/{installments_quantity})'
            parent_transaction.is_installment = True
            parent_transaction.installment_number = 1
            parent_transaction.value = installment_value
            parent_transaction.save()

            # Cria as demais parcelas
            for i in range(2, installments_quantity + 1):
                new_due_date = original_due_date + relativedelta(months=i - 1)

                installment = Transaction(
                    title=f'{original_title} ({i}/{installments_quantity})',
                    value=installment_value,
                    due_date=new_due_date,
                    transaction_type=form.cleaned_data['transaction_type'],
                    is_paid=False,
                    is_installment=True,
                    installment_number=i,
                    parent_transaction=parent_transaction
                )
                transactions_to_create.append(installment)

            Transaction.objects.bulk_create(transactions_to_create)

        return super().form_valid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        month_param = None
        year_param = None
        params = self.request.GET
        if filter_month := params.get('month'):
            month_param = filter_month
        if filter_year := params.get('year'):
            year_param = filter_year
        qs = super().get_queryset()
        if month_param:
            qs = qs.filter(due_date__month=month_param)
        if year_param:
            qs = qs.filter(due_date__year=year_param)
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
