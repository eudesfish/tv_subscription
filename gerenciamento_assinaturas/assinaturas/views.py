from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from .models import Assinatura
from .forms import AssinaturaForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum

class AssinaturaListView(ListView):
    model = Assinatura
    template_name = 'assinaturas/assinatura_list.html'
    
    def get_queryset(self):
        return Assinatura.objects.select_related('servidor').all()

class AssinaturaDetailView(DetailView):
    model = Assinatura
    template_name = 'assinaturas/assinatura_detail.html'
    
class AssinaturaCreateView(CreateView):
    model = Assinatura
    form_class = AssinaturaForm
    template_name = 'assinaturas/assinatura_form.html'
    success_url = reverse_lazy('assinaturas')
    
    def form_valid(self, form):
        cliente = form.cleaned_data['cliente']
        form.instance.telefone = cliente.telefone
        
        # Corrige a verificação de `kwargs['instance'].pk`
        if self.request.method == 'POST' and self.kwargs.get('pk'):
            instance = self.get_form_kwargs().get('instance')
            if instance and instance.pk:
                # Lógica caso a instância exista e tenha uma chave primária
                pass  # Substitua com a lógica apropriada

        return super().form_valid(form)

class AssinaturaUpdateView(UpdateView):
    model = Assinatura
    form_class = AssinaturaForm
    template_name = 'assinaturas/assinatura_form.html'

class AssinaturaDeleteView(DeleteView):
    model = Assinatura
    template_name = 'assinaturas/assinatura_confirm_delete.html'
    success_url = reverse_lazy('assinaturas')

class RelatorioView(TemplateView):
    template_name = 'assinaturas/relatorio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mes_filtro = self.request.GET.get('mes', None)
        if mes_filtro:
            ano, mes = map(int, mes_filtro.split('-'))
            data_inicio = timezone.datetime(ano, mes, 1)
            data_fim = (data_inicio + timedelta(days=31)).replace(day=1)
            assinaturas = Assinatura.objects.filter(data_inicio__gte=data_inicio, data_inicio__lt=data_fim)
        else:
            assinaturas = Assinatura.objects.all()
        
        total_valor = assinaturas.aggregate(Sum('valor'))['valor__sum']
        
        context['assinaturas'] = assinaturas
        context['total_valor'] = total_valor
        return context

def gerar_pdf(request):
    template_path = 'assinaturas/relatorio_pdf.html'
    context = {
        'assinaturas': Assinatura.objects.all(),
        'total_valor': Assinatura.objects.aggregate(Sum('valor'))['valor__sum'],
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response

def informar_pagamento(request, pk):
    assinatura = get_object_or_404(Assinatura, pk=pk)
    
    if request.method == 'POST':
        data_pagamento = request.POST.get('data_pagamento')
        
        if data_pagamento:
            data_pagamento = timezone.datetime.strptime(data_pagamento, '%Y-%m-%d').date()
            nova_assinatura = Assinatura(
                cliente=assinatura.cliente,
                telefone=assinatura.telefone,
                data_inicio=data_pagamento,
                data_vencimento=data_pagamento + timedelta(days=30),
                valor=assinatura.valor,
                observacao=assinatura.observacao,
                servidor=assinatura.servidor
            )
            nova_assinatura.save()
            
            return redirect('assinaturas')
    
    return render(request, 'assinaturas/informar_pagamento.html', {'assinatura': assinatura})
