from django.contrib import admin
from .models import (
    PerfilFinanceiro,
    GrupoFinanceiro,
    MembroGrupo,
    Conta,
    Categoria,
    Lancamento
)

admin.site.register(PerfilFinanceiro)
admin.site.register(GrupoFinanceiro)
admin.site.register(MembroGrupo)
admin.site.register(Conta)
admin.site.register(Categoria)
admin.site.register(Lancamento)