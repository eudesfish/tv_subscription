from django.urls import path
from .views import (
    AssinaturaListView,
    AssinaturaDetailView,
    AssinaturaCreateView,
    AssinaturaUpdateView,
    AssinaturaDeleteView,
    informar_pagamento,
    RelatorioView,
    gerar_pdf
)

urlpatterns = [
    path('', AssinaturaListView.as_view(), name='assinaturas'),
    path('<int:pk>/', AssinaturaDetailView.as_view(), name='assinatura_detail'),
    path('nova/', AssinaturaCreateView.as_view(), name='nova_assinatura'),
    path('<int:pk>/editar/', AssinaturaUpdateView.as_view(), name='editar_assinatura'),
    path('<int:pk>/excluir/', AssinaturaDeleteView.as_view(), name='excluir_assinatura'),
    path('<int:pk>/informar_pagamento/', informar_pagamento, name='informar_pagamento'),
    path('relatorios/', RelatorioView.as_view(), name='relatorio'),
    path('relatorios/pdf/', gerar_pdf, name='gerar_pdf'),
]
