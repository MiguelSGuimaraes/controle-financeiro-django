from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_lancamentos, name='lista_lancamentos'),
    path('novo/', views.criar_lancamento, name='criar_lancamento'),
    path('<int:pk>/', views.detalhe_lancamento, name='detalhe_lancamento'),
    path('<int:pk>/editar/', views.editar_lancamento, name='editar_lancamento'),
    path('<int:pk>/excluir/', views.excluir_lancamento, name='excluir_lancamento'),
]