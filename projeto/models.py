from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import now

class Receita(models.Model):
    titulo = models.CharField(max_length=80)
    saldo = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.titulo


class Despesa(models.Model):
    titulo = models.CharField(max_length=80)
    saldo = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.titulo


class Balancete(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    despesas = models.ManyToManyField(Despesa)
    receitas = models.ManyToManyField(Receita)
    data = models.DateField(default=now)
    referencia = models.CharField(
        primary_key=False,
        default=f"{timezone.now().month}_{timezone.now().year}",
        max_length=6
    )

    def __str__(self):
        return self.referencia

    class Meta:
        unique_together = ('referencia', 'usuario')
