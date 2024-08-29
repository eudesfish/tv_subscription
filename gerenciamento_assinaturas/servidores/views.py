# servidores/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Servidor
from .forms import ServidorForm

class ServidorListView(ListView):
    model = Servidor
    template_name = 'servidores/servidor_list.html'

class ServidorCreateView(CreateView):
    model = Servidor
    form_class = ServidorForm
    template_name = 'servidores/servidor_form.html'
    success_url = reverse_lazy('servidores')

class ServidorUpdateView(UpdateView):
    model = Servidor
    form_class = ServidorForm
    template_name = 'servidores/servidor_form.html'
    success_url = reverse_lazy('servidores')

class ServidorDeleteView(DeleteView):
    model = Servidor
    template_name = 'servidores/servidor_confirm_delete.html'
    success_url = reverse_lazy('servidores')
