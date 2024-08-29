# assinaturas/admin.py

from django.contrib import admin
from assinaturas.models import Assinatura

@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = ('get_nome_cliente', 'telefone', 'data_inicio', 'data_vencimento', 'valor')
    search_fields = ('cliente__nome', 'telefone')
    list_filter = ('data_inicio', 'data_vencimento')

    def get_nome_cliente(self, obj):
        return obj.cliente.nome
    get_nome_cliente.short_description = 'Nome do Cliente'