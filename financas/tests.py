
from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Conta, Lancamento


class TestesFinanceiros(TestCase):

    def setUp(self):
        # Cria o primeiro usuário
        self.usuario = User.objects.create_user(
            username='usuario_teste',
            password='senha123'
        )

        # Cria uma conta individual
        self.conta = Conta.objects.create(
            nome='Conta principal',
            tipo='CORRENTE',
            saldo_inicial=Decimal('100.00'),
            usuario=self.usuario
        )

        # Cria uma receita
        self.receita = Lancamento.objects.create(
            descricao='Salário',
            categoria='SALARIO',
            conta=self.conta,
            tipo='R',
            forma_pagamento='PIX',
            valor=Decimal('200.00'),
            data_lancamento=date(2026, 11, 1)
        )

        # Cria uma despesa
        self.despesa = Lancamento.objects.create(
            descricao='Mercado',
            categoria='ALIMENTACAO',
            conta=self.conta,
            tipo='D',
            forma_pagamento='DINHEIRO',
            valor=Decimal('50.00'),
            data_lancamento=date(2026, 11, 2)
        )

    def test_criacao_de_lancamento(self):
        """Verifica se um lançamento é criado corretamente."""

        lancamento = Lancamento.objects.get(
            descricao='Salário'
        )

        self.assertEqual(lancamento.valor, Decimal('200.00'))
        self.assertEqual(lancamento.tipo, 'R')
        self.assertEqual(lancamento.conta, self.conta)

    def test_calculo_do_saldo_no_dashboard(self):
        """Verifica se o dashboard calcula corretamente o saldo."""

        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse('dashboard'))

        self.assertEqual(resposta.status_code, 200)

        # Saldo inicial + receitas - despesas
        self.assertEqual(
            resposta.context['saldo_total'],
            Decimal('250.00')
        )

    def test_usuario_nao_visualiza_lancamentos_de_outro_usuario(self):
        """Verifica se os lançamentos de outros usuários ficam protegidos."""

        outro_usuario = User.objects.create_user(
            username='outro_usuario',
            password='senha123'
        )

        outra_conta = Conta.objects.create(
            nome='Conta privada',
            tipo='CORRENTE',
            saldo_inicial=Decimal('0.00'),
            usuario=outro_usuario
        )

        Lancamento.objects.create(
            descricao='Despesa secreta',
            categoria='OUTROS',
            conta=outra_conta,
            tipo='D',
            forma_pagamento='PIX',
            valor=Decimal('999.00'),
            data_lancamento=date(2026, 11, 3)
        )

        self.client.force_login(self.usuario)

        resposta = self.client.get(
            reverse('lista_lancamentos')
        )

        self.assertEqual(resposta.status_code, 200)

        self.assertContains(resposta, 'Salário')
        self.assertContains(resposta, 'Mercado')
        self.assertNotContains(resposta, 'Despesa secreta')
