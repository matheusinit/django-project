from django.contrib import admin
from .models import Receita, Despesa, Balancete

class DespesaInline(admin.TabularInline):
    model = Balancete.despesas.through
    extra = 1

class ReceitaInline(admin.TabularInline):
    model = Balancete.receitas.through
    extra = 1

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    fields = ['titulo', 'saldo']
    list_display = ['titulo', 'saldo']
    search_fields = ['titulo']

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    fields = ['titulo', 'saldo']
    list_display = ['titulo', 'saldo']
    search_fields = ['titulo']


class BalanceteAdmin(admin.ModelAdmin):
    inlines = [DespesaInline, ReceitaInline]
    exclude = ['despesas', 'receitas']

admin.site.register(Balancete, BalanceteAdmin)