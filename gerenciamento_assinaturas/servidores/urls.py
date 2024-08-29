# servidores/urls.py

from django.urls import path
from .views import ServidorListView, ServidorCreateView, ServidorUpdateView, ServidorDeleteView

urlpatterns = [
    path('', ServidorListView.as_view(), name='servidores'),
    path('novo/', ServidorCreateView.as_view(), name='novo_servidor'),
    path('<int:pk>/editar/', ServidorUpdateView.as_view(), name='editar_servidor'),
    path('<int:pk>/excluir/', ServidorDeleteView.as_view(), name='excluir_servidor'),
]
