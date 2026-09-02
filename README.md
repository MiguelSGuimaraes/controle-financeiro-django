# Controle Financeiro Pessoal — CRUD em Django

Trabalho da disciplina de Programação Back-End — Centro Universitário de Itajubá (FEPI).

## Integrante

- Miguel

## Tema

Sistema de controle financeiro pessoal, permitindo o cadastro de lançamentos (receitas e despesas), com categoria, forma de pagamento, valor, data e observações.

## Model: `Lancamento`

| Campo | Tipo | Descrição |
|---|---|---|
| `descricao` | CharField | Descrição curta do lançamento |
| `categoria` | CharField (choices) | Categoria do lançamento (Alimentação, Transporte, etc.) |
| `tipo` | CharField (choices) | Receita ou Despesa |
| `forma_pagamento` | CharField (choices) | Forma de pagamento (Dinheiro, Pix, Cartão, etc.) |
| `observacoes` | TextField | Observações adicionais (opcional) |
| `valor` | DecimalField | Valor do lançamento |
| `data_lancamento` | DateField | Data em que o lançamento ocorreu |
| `recorrente` | BooleanField | Indica se o lançamento se repete mensalmente |

## Funcionalidades

- Listagem de lançamentos
- Cadastro de novo lançamento
- Visualização de detalhes
- Edição de lançamento existente
- Exclusão com tela de confirmação
- Gerenciamento via Django Admin

## Tecnologias

- Python
- Django
- SQLite (banco de dados padrão de desenvolvimento)

## Como executar o projeto

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Aplique as migrations:
```bash
python manage.py migrate
```

5. (Opcional) Crie um superusuário para acessar o Admin:
```bash
python manage.py createsuperuser
```

6. Execute o servidor:
```bash
python manage.py runserver
```

7. Acesse no navegador:
- CRUD: http://127.0.0.1:8000/lancamentos/
- Admin: http://127.0.0.1:8000/admin/