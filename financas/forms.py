from django import forms
from .models import Lancamento


class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = [
            'descricao',
            'categoria',
            'conta',
            'tipo',
            'forma_pagamento',
            'observacoes',
            'valor',
            'data_lancamento',
            'recorrente',
        ]

        widgets = {
            'data_lancamento': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'observacoes': forms.Textarea(
                attrs={'rows': 3}
            ),
        }