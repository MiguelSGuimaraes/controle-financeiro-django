from django.db import models

# Create your models here.
class Lancamento(models.Model):

    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]

    CATEGORIA_CHOICES = [
        ('ALIMENTACAO', 'Alimentação'),
        ('TRANSPORTE', 'Transporte'),
        ('MORADIA', 'Moradia'),
        ('LAZER', 'Lazer'),
        ('SAUDE', 'Saúde'),
        ('EDUCACAO', 'Educação'),
        ('SALARIO', 'Salário'),
        ('OUTROS', 'Outros'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('PIX', 'Pix'),
        ('TRANSFERENCIA', 'Transferência'),
    ]

    descricao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    observacoes = models.TextField(blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_lancamento = models.DateField()
    recorrente = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data_lancamento']
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"