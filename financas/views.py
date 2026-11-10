
import csv

from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from django.http import HttpResponse
from decimal import Decimal

from .models import Lancamento, Conta, Categoria
from .forms import LancamentoForm, ContaForm, CategoriaForm


@login_required
def lista_lancamentos(request):
    lancamentos = Lancamento.objects.filter(
        conta__usuario=request.user,
        conta__grupo__isnull=True
    )

    totais = lancamentos.aggregate(
        receitas=Sum('valor', filter=Q(tipo='R')),
        despesas=Sum('valor', filter=Q(tipo='D'))
    )

    total_receitas = totais['receitas'] or Decimal('0.00')
    total_despesas = totais['despesas'] or Decimal('0.00')

    saldo = total_receitas - total_despesas

    contexto = {
        'lancamentos': lancamentos.order_by(
            '-data_lancamento', '-id'
        ),
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
    }

    return render(
        request,
        'financas/lista_lancamentos.html',
        contexto
    )


@login_required
def detalhe_lancamento(request, pk):
    lancamento = get_object_or_404(
        Lancamento,
        pk=pk,
        conta__usuario=request.user,
        conta__grupo__isnull=True
    )

    return render(
        request,
        'financas/detalhe_lancamento.html',
        {'lancamento': lancamento}
    )


@login_required
def criar_lancamento(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST, usuario=request.user)

        if form.is_valid():
            form.save()
            return redirect('lista_lancamentos')
    else:
        form = LancamentoForm(usuario=request.user)

    return render(
        request,
        'financas/form_lancamento.html',
        {'form': form}
    )


@login_required
def editar_lancamento(request, pk):
    lancamento = get_object_or_404(
        Lancamento,
        pk=pk,
        conta__usuario=request.user,
        conta__grupo__isnull=True
    )

    if request.method == 'POST':
        form = LancamentoForm(
            request.POST,
            instance=lancamento,
            usuario=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('lista_lancamentos')
    else:
        form = LancamentoForm(
            instance=lancamento,
            usuario=request.user
        )

    return render(
        request,
        'financas/form_lancamento.html',
        {'form': form}
    )


@login_required
def excluir_lancamento(request, pk):
    lancamento = get_object_or_404(
        Lancamento,
        pk=pk,
        conta__usuario=request.user,
        conta__grupo__isnull=True
    )

    if request.method == 'POST':
        lancamento.delete()
        return redirect('lista_lancamentos')

    return render(
        request,
        'financas/confirmar_exclusao.html',
        {'lancamento': lancamento}
    )


@login_required
def lista_contas(request):
    contas = Conta.objects.filter(
        usuario=request.user,
        grupo__isnull=True
    )

    return render(
        request,
        'financas/lista_contas.html',
        {'contas': contas}
    )


@login_required
def criar_conta(request):
    if request.method == 'POST':
        form = ContaForm(request.POST)

        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.grupo = None
            conta.save()

            return redirect('lista_contas')
    else:
        form = ContaForm()

    return render(
        request,
        'financas/form_conta.html',
        {'form': form}
    )


@login_required
def editar_conta(request, pk):
    conta = get_object_or_404(
        Conta,
        pk=pk,
        usuario=request.user,
        grupo__isnull=True
    )

    if request.method == 'POST':
        form = ContaForm(request.POST, instance=conta)

        if form.is_valid():
            form.save()
            return redirect('lista_contas')
    else:
        form = ContaForm(instance=conta)

    return render(
        request,
        'financas/form_conta.html',
        {'form': form}
    )


@login_required
def excluir_conta(request, pk):
    conta = get_object_or_404(
        Conta,
        pk=pk,
        usuario=request.user,
        grupo__isnull=True
    )

    if request.method == 'POST':
        try:
            conta.delete()
            messages.success(request, 'Conta excluída com sucesso.')
        except ProtectedError:
            messages.error(
                request,
                'Esta conta possui lançamentos vinculados e não pode ser excluída.'
            )

        return redirect('lista_contas')

    return render(
        request,
        'financas/confirmar_exclusao.html',
        {'conta': conta}
    )


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.filter(
        usuario=request.user,
        grupo__isnull=True
    )

    return render(
        request,
        'financas/lista_categorias.html',
        {'categorias': categorias}
    )


@login_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)

        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.grupo = None
            categoria.save()

            return redirect('lista_categorias')
    else:
        form = CategoriaForm()

    return render(
        request,
        'financas/form_categoria.html',
        {'form': form}
    )


@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(
        Categoria,
        pk=pk,
        usuario=request.user,
        grupo__isnull=True
    )

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)

        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(
        request,
        'financas/form_categoria.html',
        {'form': form}
    )


@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(
        Categoria,
        pk=pk,
        usuario=request.user,
        grupo__isnull=True
    )

    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoria excluída com sucesso.')
        except ProtectedError:
            messages.error(
                request,
                'Esta categoria possui lançamentos vinculados e não pode ser excluída.'
            )

        return redirect('lista_categorias')

    return render(
        request,
        'financas/confirmar_exclusao.html',
        {'categoria': categoria}
    )


@login_required
def dashboard(request):
    contas = Conta.objects.filter(
        usuario=request.user,
        grupo__isnull=True
    )

    lancamentos = Lancamento.objects.filter(conta__in=contas)

    saldo_inicial = contas.aggregate(
        total=Sum('saldo_inicial')
    )['total'] or Decimal('0.00')

    totais = lancamentos.aggregate(
        receitas=Sum('valor', filter=Q(tipo='R')),
        despesas=Sum('valor', filter=Q(tipo='D'))
    )

    receitas = totais['receitas'] or Decimal('0.00')
    despesas = totais['despesas'] or Decimal('0.00')

    saldo_total = saldo_inicial + receitas - despesas

    hoje = timezone.localdate()

    lancamentos_mes = lancamentos.filter(
        data_lancamento__year=hoje.year,
        data_lancamento__month=hoje.month
    )

    totais_mes = lancamentos_mes.aggregate(
        receitas=Sum('valor', filter=Q(tipo='R')),
        despesas=Sum('valor', filter=Q(tipo='D'))
    )

    receitas_mes = totais_mes['receitas'] or Decimal('0.00')
    despesas_mes = totais_mes['despesas'] or Decimal('0.00')

    resultado_mes = receitas_mes - despesas_mes

    ultimos_lancamentos = lancamentos.order_by(
        '-data_lancamento', '-id'
    )[:5]

    nomes_meses = [
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
    ]

    indice_mes = hoje.year * 12 + hoje.month - 1 - 5
    ano_inicio = indice_mes // 12
    mes_inicio = indice_mes % 12 + 1

    data_inicio = hoje.replace(
        year=ano_inicio,
        month=mes_inicio,
        day=1
    )

    dados_mensais = (
        lancamentos
        .filter(
            data_lancamento__gte=data_inicio,
            data_lancamento__lte=hoje
        )
        .annotate(mes=TruncMonth('data_lancamento'))
        .values('mes')
        .annotate(
            receitas=Sum('valor', filter=Q(tipo='R')),
            despesas=Sum('valor', filter=Q(tipo='D'))
        )
        .order_by('mes')
    )

    valores_por_mes = {}

    for item in dados_mensais:
        mes = item['mes']

        valores_por_mes[(mes.year, mes.month)] = {
            'receitas': item['receitas'] or Decimal('0.00'),
            'despesas': item['despesas'] or Decimal('0.00')
        }

    grafico_labels = []
    grafico_receitas = []
    grafico_despesas = []

    for i in range(5, -1, -1):
        indice = hoje.year * 12 + hoje.month - 1 - i

        ano = indice // 12
        mes = indice % 12 + 1

        valores = valores_por_mes.get(
            (ano, mes),
            {
                'receitas': Decimal('0.00'),
                'despesas': Decimal('0.00')
            }
        )

        grafico_labels.append(
            f'{nomes_meses[mes - 1]}/{ano}'
        )

        grafico_receitas.append(float(valores['receitas']))
        grafico_despesas.append(float(valores['despesas']))

    contexto = {
        'saldo_total': saldo_total,
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'resultado_mes': resultado_mes,
        'ultimos_lancamentos': ultimos_lancamentos,
        'grafico_labels': grafico_labels,
        'grafico_receitas': grafico_receitas,
        'grafico_despesas': grafico_despesas,
    }

    return render(
        request,
        'financas/dashboard.html',
        contexto
    )


@login_required
def consultas(request):
    lancamentos = Lancamento.objects.filter(
        conta__usuario=request.user,
        conta__grupo__isnull=True
    )

    data_inicio = parse_date(request.GET.get('data_inicio', ''))
    data_fim = parse_date(request.GET.get('data_fim', ''))

    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')

    if data_inicio:
        lancamentos = lancamentos.filter(
            data_lancamento__gte=data_inicio
        )

    if data_fim:
        lancamentos = lancamentos.filter(
            data_lancamento__lte=data_fim
        )

    if tipo in ['R', 'D']:
        lancamentos = lancamentos.filter(tipo=tipo)

    categorias_validas = [
        escolha[0] for escolha in Lancamento.CATEGORIA_CHOICES
    ]

    if categoria in categorias_validas:
        lancamentos = lancamentos.filter(categoria=categoria)

    totais = lancamentos.aggregate(
        receitas=Sum('valor', filter=Q(tipo='R')),
        despesas=Sum('valor', filter=Q(tipo='D'))
    )

    receitas = totais['receitas'] or Decimal('0.00')
    despesas = totais['despesas'] or Decimal('0.00')

    contexto = {
        'lancamentos': lancamentos.order_by(
            '-data_lancamento', '-id'
        ),
        'data_inicio': request.GET.get('data_inicio', ''),
        'data_fim': request.GET.get('data_fim', ''),
        'tipo_selecionado': tipo,
        'categoria_selecionada': categoria,
        'categorias': Lancamento.CATEGORIA_CHOICES,
        'receitas': receitas,
        'despesas': despesas,
        'resultado': receitas - despesas,
    }

    return render(
        request,
        'financas/consultas.html',
        contexto
    )


@login_required
def exportar_consultas_csv(request):
    lancamentos = Lancamento.objects.filter(
        conta__usuario=request.user,
        conta__grupo__isnull=True
    )

    data_inicio = parse_date(request.GET.get('data_inicio', ''))
    data_fim = parse_date(request.GET.get('data_fim', ''))

    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')

    if data_inicio:
        lancamentos = lancamentos.filter(
            data_lancamento__gte=data_inicio
        )

    if data_fim:
        lancamentos = lancamentos.filter(
            data_lancamento__lte=data_fim
        )

    if tipo in ['R', 'D']:
        lancamentos = lancamentos.filter(tipo=tipo)

    categorias_validas = [
        escolha[0] for escolha in Lancamento.CATEGORIA_CHOICES
    ]

    if categoria in categorias_validas:
        lancamentos = lancamentos.filter(categoria=categoria)

    totais = lancamentos.aggregate(
        receitas=Sum('valor', filter=Q(tipo='R')),
        despesas=Sum('valor', filter=Q(tipo='D'))
    )

    receitas = totais['receitas'] or Decimal('0.00')
    despesas = totais['despesas'] or Decimal('0.00')

    resposta = HttpResponse(
        content_type='text/csv; charset=utf-8'
    )

    resposta['Content-Disposition'] = (
        'attachment; filename="relatorio_financeiro.csv"'
    )

    resposta.write('\ufeff')

    escritor = csv.writer(resposta, delimiter=';')

    def formatar_valor(valor):
        return f'{valor:.2f}'.replace('.', ',')

    escritor.writerow([
        'ID',
        'Data',
        'Tipo',
        'Categoria',
        'Valor'
    ])

    for lancamento in lancamentos.order_by(
        '-data_lancamento', '-id'
    ):
        escritor.writerow([
            lancamento.id,
            lancamento.data_lancamento.strftime('%d/%m/%Y'),
            lancamento.get_tipo_display(),
            lancamento.categoria,
            formatar_valor(lancamento.valor)
        ])

    escritor.writerow([])
    escritor.writerow(['RESUMO FINANCEIRO'])
    escritor.writerow(['Total de receitas', formatar_valor(receitas)])
    escritor.writerow(['Total de despesas', formatar_valor(despesas)])
    escritor.writerow(['Resultado', formatar_valor(receitas - despesas)])

    return resposta
