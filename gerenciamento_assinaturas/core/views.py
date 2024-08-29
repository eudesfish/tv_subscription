# core/views.py

from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from assinaturas.models import Assinatura
from clientes.models import Cliente
from servidores.models import Servidor
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.shortcuts import render

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'

class ServidorListView(ListView):
    model = Servidor
    template_name = 'servidores/servidor_list.html'
    context_object_name = 'servidores'

class AssinaturaListView(ListView):
    model = Assinatura
    template_name = 'assinaturas/assinatura_list.html'
    context_object_name = 'assinaturas'

class InformarPagamentoView(UpdateView):
    model = Assinatura
    fields = ['data_vencimento', 'observacao']
    template_name = 'assinaturas/informar_pagamento.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        assinatura = form.instance
        assinatura.data_vencimento += timedelta(days=30)
        assinatura.save()
        return response

    def get_success_url(self):
        return redirect('assinaturas')

def dashboard(request):
    total_clientes = Cliente.objects.count()
    tres_dias = timedelta(days=3)
    data_futura = timezone.now() + tres_dias
    total_assinaturas_a_vencer = Assinatura.objects.filter(data_vencimento__lte=data_futura).count()

    context = {
        'total_clientes': total_clientes,
        'total_assinaturas_a_vencer': total_assinaturas_a_vencer
    }
    return render(request, 'core/dashboard.html', context)
