from django.contrib import admin
from .models import Categoria, Conta, Lancamento, Orcamento


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor')
    search_fields = ('nome',)


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'banco', 'tipo', 'saldo_inicial')
    list_filter = ('tipo',)
    search_fields = ('nome', 'banco')


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'categoria',
        'conta',
        'tipo',
        'forma_pagamento',
        'valor',
        'data_lancamento',
        'recorrente',
    )
    list_filter = (
        'tipo',
        'categoria',
        'conta',
        'forma_pagamento',
        'recorrente',
    )
    search_fields = ('descricao',)


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = (
        'categoria',
        'mes',
        'ano',
        'valor_limite',
    )
    list_filter = ('mes', 'ano', 'categoria')
# Register your models here.
