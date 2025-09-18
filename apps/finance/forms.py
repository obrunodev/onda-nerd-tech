from apps.finance.models import Transaction

from django import forms


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['title', 'value', 'due_date']
