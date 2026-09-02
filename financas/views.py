from django.shortcuts import render, redirect, get_object_or_404
from .models import Lancamento
from .forms import LancamentoForm


def lista_lancamentos(request):
    lancamentos = Lancamento.objects.all()
    return render(request, 'financas/lista_lancamentos.html', {'lancamentos': lancamentos})


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