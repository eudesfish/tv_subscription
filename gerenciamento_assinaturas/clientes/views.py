# clientes/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cliente
from .forms import ClienteForm

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'  # Nome do template para renderizar a lista
    context_object_name = 'clientes'  # Nome do contexto no template
    
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = '/clientes/'

class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = ['nome', 'telefone', 'cidade', 'observacao']
    template_name = 'clientes/cliente_form.html'

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes')