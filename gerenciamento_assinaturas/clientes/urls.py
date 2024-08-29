# clientes/urls.py
from django.urls import path
from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView
)

urlpatterns = [
    path('', ClienteListView.as_view(), name='clientes'),
    path('novo/', ClienteCreateView.as_view(), name='novo_cliente'),
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('<int:pk>/excluir/', ClienteDeleteView.as_view(), name='excluir_cliente'),
]
