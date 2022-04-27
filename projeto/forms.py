from django import forms
from django.contrib.auth.models import User


class DespesaForm(forms.Form):
    titulo = forms.CharField(max_length=80)
    saldo = forms.DecimalField(decimal_places=2, max_digits=6)


class ReceitaForm(forms.Form):
    titulo = forms.CharField(max_length=80)
    saldo = forms.DecimalField(decimal_places=2, max_digits=6)


class UsuarioForm(forms.Form):
    nome = forms.CharField(max_length=55)
    senha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
