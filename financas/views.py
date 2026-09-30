from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Lancamento
from .forms import LancamentoForm

def lista_lancamentos(request):
    lancamentos = Lancamento.objects.all()

    total_receitas = Lancamento.objects.filter(
        tipo='R'
    ).aggregate(total=Sum('valor'))['total'] or 0

    total_despesas = Lancamento.objects.filter(
        tipo='D'
    ).aggregate(total=Sum('valor'))['total'] or 0

    total_guardado = Lancamento.objects.filter(
        tipo='G'
    ).aggregate(total=Sum('valor'))['total'] or 0

    saldo = total_receitas - total_despesas - total_guardado

    return render(request, 'financas/lista_lancamentos.html', {
        'lancamentos': lancamentos,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
    })


def detalhe_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    return render(request, 'financas/detalhe_lancamento.html', {'lancamento': lancamento})


def criar_lancamento(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_lancamentos')
    else:
        form = LancamentoForm()
    return render(request, 'financas/form_lancamento.html', {'form': form})


def editar_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    if request.method == 'POST':
        form = LancamentoForm(request.POST, instance=lancamento)
        if form.is_valid():
            form.save()
            return redirect('lista_lancamentos')
    else:
        form = LancamentoForm(instance=lancamento)
    return render(request, 'financas/form_lancamento.html', {'form': form})


def excluir_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    if request.method == 'POST':
        lancamento.delete()
        return redirect('lista_lancamentos')
    return render(request, 'financas/confirmar_exclusao.html', {'lancamento': lancamento})


def dashboard(request):
    receitas = Lancamento.objects.filter(
        tipo='R'
    ).aggregate(total=Sum('valor'))['total'] or 0

    despesas = Lancamento.objects.filter(
        tipo='D'
    ).aggregate(total=Sum('valor'))['total'] or 0

    guardado = Lancamento.objects.filter(
        tipo='G'
    ).aggregate(total=Sum('valor'))['total'] or 0

    saldo = receitas - despesas - guardado

    ultimos_lancamentos = Lancamento.objects.all()[:5]

    contexto = {
        'receitas': receitas,
        'despesas': despesas,
        'guardado': guardado,
        'saldo': saldo,
        'ultimos_lancamentos': ultimos_lancamentos,
    }

    return render(
        request,
        'financas/dashboard.html',
        contexto
    )