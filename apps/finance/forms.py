from apps.finance.models import Transaction

from django import forms


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['title', 'value', 'due_date']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
