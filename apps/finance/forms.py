from apps.finance.models import Transaction

from django import forms


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['title', 'value', 'due_date', 'transaction_type']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
            "transaction_type": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
