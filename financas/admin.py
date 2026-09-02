from django.contrib import admin
from .models import Lancamento


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'categoria', 'tipo', 'valor', 'data_lancamento', 'recorrente')
    list_filter = ('tipo', 'categoria', 'recorrente')
    search_fields = ('descricao',)

# Register your models here.
