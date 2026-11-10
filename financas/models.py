
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class PerfilFinanceiro(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_financeiro'
    )
    telefone = models.CharField(max_length=20, blank=True)
    objetivo_mensal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class GrupoFinanceiro(models.Model):
    nome = models.CharField(max_length=100)
    criado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='grupos_criados'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    membros = models.ManyToManyField(
        User,
        through='MembroGrupo',
        related_name='grupos_financeiros'
    )

    def __str__(self):
        return self.nome


class MembroGrupo(models.Model):

    PAPEL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('MEMBRO', 'Membro'),
    ]

    grupo = models.ForeignKey(
        GrupoFinanceiro,
        on_delete=models.CASCADE,
        related_name='participacoes'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='participacoes_financeiras'
    )
    papel = models.CharField(
        max_length=10,
        choices=PAPEL_CHOICES,
        default='MEMBRO'
    )
    data_entrada = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['grupo', 'usuario'],
                name='unico_usuario_por_grupo'
            )
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.grupo.nome}"


class Conta(models.Model):

    TIPO_CHOICES = [
        ('CORRENTE', 'Conta Corrente'),
        ('POUPANCA', 'Poupança'),
        ('CARTEIRA', 'Carteira'),
        ('DINHEIRO', 'Dinheiro'),
        ('INVESTIMENTO', 'Investimento'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    saldo_inicial = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contas_individuais'
    )

    grupo = models.ForeignKey(
        GrupoFinanceiro,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contas'
    )

    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(usuario__isnull=False, grupo__isnull=True) |
                    Q(usuario__isnull=True, grupo__isnull=False)
                ),
                name='conta_de_usuario_ou_grupo'
            )
        ]

    def __str__(self):
        return self.nome


class Categoria(models.Model):

    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]

    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='categorias_individuais'
    )

    grupo = models.ForeignKey(
        GrupoFinanceiro,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='categorias'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(usuario__isnull=False, grupo__isnull=True) |
                    Q(usuario__isnull=True, grupo__isnull=False)
                ),
                name='categoria_de_usuario_ou_grupo'
            )
        ]

    def __str__(self):
        return self.nome


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

    # Campo antigo mantido para preservar os dados existentes.
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES
    )

    # Novos relacionamentos, inicialmente opcionais.
    categoria_relacionada = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='lancamentos'
    )

    conta = models.ForeignKey(
        Conta,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='lancamentos'
    )

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES
    )
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
