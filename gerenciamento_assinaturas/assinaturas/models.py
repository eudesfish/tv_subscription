from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from clientes.models import Cliente
from servidores.models import Servidor

class Assinatura(models.Model):
    codigo_identificacao = models.CharField(max_length=6, unique=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True)
    data_inicio = models.DateField()
    data_vencimento = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Gera o código de identificação se não existir
        if not self.codigo_identificacao:
            last_assinatura = Assinatura.objects.all().order_by('id').last()
            if last_assinatura and last_assinatura.codigo_identificacao.isdigit():
                last_code = int(last_assinatura.codigo_identificacao)
                self.codigo_identificacao = f'{last_code + 1:06d}'
            else:
                self.codigo_identificacao = '000001'
        
        # Herda o telefone do cliente
        if self.cliente and not self.telefone:
            self.telefone = self.cliente.telefone

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cliente.nome} - {self.data_vencimento}'

    def informar_pagamento(self):
        # Cria uma nova assinatura com novos ciclo e ID
        nova_data_inicio = timezone.now().date()
        nova_data_vencimento = nova_data_inicio + timedelta(days=30)
        nova_assinatura = Assinatura(
            cliente=self.cliente,
            servidor=self.servidor,
            telefone=self.telefone,
            data_inicio=nova_data_inicio,
            data_vencimento=nova_data_vencimento,
            valor=self.valor,
            observacao=self.observacao
        )
        nova_assinatura.save()
        return nova_assinatura

    def clean(self):
        if self.data_inicio >= self.data_vencimento:
            raise ValidationError('A data de início deve ser anterior à data de vencimento.')

    def get_absolute_url(self):
        if self.pk:  # Verifica se a instância já foi salva
            return reverse('assinatura_detail', kwargs={'pk': self.pk})
        return reverse('assinaturas')  # Redireciona para a lista de assinaturas caso ainda não tenha sido salva
