
from django.urls import path
from . import views

urlpatterns = [

    path('', views.lista_lancamentos, name='lista_lancamentos'),
    path('novo/', views.criar_lancamento, name='criar_lancamento'),
    path('<int:pk>/', views.detalhe_lancamento, name='detalhe_lancamento'),
    path('<int:pk>/editar/', views.editar_lancamento, name='editar_lancamento'),
    path('<int:pk>/excluir/', views.excluir_lancamento, name='excluir_lancamento'),
    path('consultas/', views.consultas, name='consultas'),

    path('contas/', views.lista_contas, name='lista_contas'),
    path('contas/nova/', views.criar_conta, name='criar_conta'),
    path('contas/<int:pk>/editar/', views.editar_conta, name='editar_conta'),
    path('contas/<int:pk>/excluir/', views.excluir_conta, name='excluir_conta'),

  
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),

    
]
