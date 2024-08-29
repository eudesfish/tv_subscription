# assinaturas/forms.py

from django import forms
from .models import Assinatura
from clientes.models import Cliente
from servidores.models import Servidor

class AssinaturaForm(forms.ModelForm):
    class Meta:
        model = Assinatura
        fields = ['cliente', 'data_inicio', 'data_vencimento', 'valor', 'observacao', 'servidor']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.pk:
            # Se estamos editando uma instância existente, o cliente deve ser somente leitura
            self.fields['cliente'].widget.attrs['readonly'] = True
            # O campo 'telefone' é derivado e não precisa ser incluído no formulário
            self.fields['telefone'].widget.attrs['readonly'] = True
