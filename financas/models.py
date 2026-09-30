from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(
        max_length=7,
        default='#3b82f6',
        help_text='Código hexadecimal, ex: #3b82f6'
    )

    class Meta:
        ordering = ['nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Conta(models.Model):
    TIPO_CONTA_CHOICES = [
        ('CORRENTE', 'Conta Corrente'),
        ('POUPANCA', 'Poupança'),
        ('CARTEIRA', 'Carteira'),
        ('INVESTIMENTO', 'Investimento'),
    ]

    nome = models.CharField(max_length=50)
    banco = models.CharField(max_length=50, blank=True)
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_CONTA_CHOICES,
        default='CORRENTE'
    )
    saldo_inicial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ['nome']
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    def __str__(self):
        return self.nome


class Lancamento(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
        ('G', 'Guardar'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('PIX', 'Pix'),
        ('TRANSFERENCIA', 'Transferência'),
        ('CAIXINHA', 'Caixinha'),
    ]

    descricao = models.CharField(max_length=100)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='lancamentos'
    )

    conta = models.ForeignKey(
        Conta,
        on_delete=models.PROTECT,
        related_name='lancamentos'
    )

    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CHOICES
    )

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES
    )

    observacoes = models.TextField(blank=True)

    valor = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    data_lancamento = models.DateField()

    recorrente = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data_lancamento']
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"


class Orcamento(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='orcamentos'
    )

    mes = models.PositiveSmallIntegerField()
    ano = models.PositiveSmallIntegerField()

    valor_limite = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    class Meta:
        ordering = ['-ano', '-mes']
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        unique_together = ['categoria', 'mes', 'ano']

    def __str__(self):
        return f"{self.categoria.nome} - {self.mes}/{self.ano}"