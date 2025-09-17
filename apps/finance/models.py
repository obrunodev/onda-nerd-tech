from apps.shared.models import BaseModel

from django.db import models


class Transaction(BaseModel):
    title = models.CharField('Título', max_length=255)
    value = models.DecimalField('Valor', decimal_places=2, max_digits=10)
    due_date = models.DateField('Data de vencimento', blank=True, null=True)
    payment_date = models.DateTimeField('Data/Hora do pagamento', blank=True, null=True)
    is_paid = models.BooleanField('Está pago?', default=False)

    class Meta:
        ordering = ['due_date']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    def __str__(self):
        return f'{self.title}: R$ {self.value}'
