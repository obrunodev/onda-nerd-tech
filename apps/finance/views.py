from apps.finance.models import Transaction
from apps.finance.forms import TransactionForm

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('finance:list')


class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transactions'


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('finance:list')


class TransactionDeleteView(DeleteView):
    model = Transaction
    success_url = reverse_lazy('finance:list')
