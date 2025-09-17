from apps.finance.models import Transaction

from django.views.generic import CreateView, ListView, UpdateView, DeleteView


class TransactionCreateView(CreateView):
    ...


class TransactionListView(ListView):
    ...


class TransactionUpdateView(UpdateView):
    ...


class TransactionDeleteView(DeleteView):
    ...
