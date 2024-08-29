from django.db import models

class Servidor(models.Model):
    nome = models.CharField(max_length=100)
    tipo_plano = models.CharField(max_length=100)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome
