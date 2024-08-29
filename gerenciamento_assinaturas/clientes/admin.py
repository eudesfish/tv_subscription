from django.contrib import admin
from clientes.models import Cliente
from servidores.models import Servidor  
#from assinaturas.models import Assinatura

admin.site.register(Cliente)
admin.site.register(Servidor)
#admin.site.register(Assinatura)