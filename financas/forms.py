
from django import forms
from .models import Lancamento, Conta, Categoria


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo', 'saldo_inicial', 'ativa']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']


class LancamentoForm(forms.ModelForm):

    class Meta:
        model = Lancamento
        fields = [
            'descricao',
            'categoria',
            'categoria_relacionada',
            'conta',
            'tipo',
            'forma_pagamento',
            'observacoes',
            'valor',
            'data_lancamento',
            'recorrente'
        ]

        widgets = {
            'data_lancamento': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'observacoes': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Todo lançamento precisa estar vinculado a uma conta.
        self.fields['conta'].required = True

        if usuario:
            # Exibe somente as contas individuais do usuário.
            self.fields['conta'].queryset = Conta.objects.filter(
                usuario=usuario,
                grupo__isnull=True
            )

            # Exibe somente as categorias individuais do usuário.
            self.fields['categoria_relacionada'].queryset = (
                Categoria.objects.filter(
                    usuario=usuario,
                    grupo__isnull=True
                )
            )
