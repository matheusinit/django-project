from django.utils import timezone
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from .models import Despesa, Receita, Balancete
from .forms import DespesaForm, ReceitaForm, UsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.db.models import Sum


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login?next=%s' % (request.path))

        try:
            balancete_do_mes = Balancete.objects.get(
                usuario=request.user,
                referencia=f"{timezone.now().month}_{timezone.now().year}"
            )

            despesas_valor_total = balancete_do_mes.despesas.aggregate(
                Sum('saldo'))
            despesas_valor_total = despesas_valor_total['saldo__sum'] or 0

            receitas_valor_total = balancete_do_mes.receitas.aggregate(
                Sum('saldo'))
            receitas_valor_total = receitas_valor_total['saldo__sum'] or 0

            valor_total = receitas_valor_total - despesas_valor_total

            context = {
                'balancete_do_mes': balancete_do_mes,
                'receitas_list': balancete_do_mes.receitas.all(),
                'receitas_count': balancete_do_mes.receitas.all().count,
                'receitas_total': receitas_valor_total,
                'despesas_list': balancete_do_mes.despesas.all(),
                'despesas_count': balancete_do_mes.despesas.all().count,
                'despesas_total': despesas_valor_total,
                'valor_total': valor_total
            }
        except Exception:
            balancete_do_mes = None

            context = {
                'balancete_do_mes': balancete_do_mes,
            }

        return render(
            request,
            'projeto/index.html',
            context
        )


class MostrarDespesasView(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            todas_despesas = Balancete.objects.get(
                usuario=request.user,
                referencia=f"{timezone.now().month}_{timezone.now().year}"
            ).despesas.order_by('titulo')

        except Balancete.DoesNotExist:
            todas_despesas = None

        except Despesa.DoesNotExist:
            raise Http404("Despesa não existe")

        return render(
            request,
            'projeto/mostrar_despesas.html',
            {'despesas': todas_despesas}
        )


class MostrarReceitasView(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            todas_receitas = Balancete.objects.get(
                usuario=request.user,
                referencia=f"{timezone.now().month}_{timezone.now().year}"
            ).receitas.order_by('titulo')
        except Balancete.DoesNotExist:
            todas_receitas = None

        except Despesa.DoesNotExist:
            raise Http404("Receita não existe")

        return render(
            request,
            'projeto/mostrar_receitas.html',
            {'receitas': todas_receitas}
        )


class MostrarBalancetesView(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            todos_balancetes = Balancete.objects.filter(
                usuario=request.user
            ).order_by('-data')

            context = {
                'balancetes': todos_balancetes
            }
        except Balancete.DoesNotExist:
            raise Http404("Balancete não existe")

        return render(request, 'projeto/mostrar_balancetes.html', context)

    def post(self, request, *args, **kwargs):
        return render(request)


class MostrarBalanceteView(generic.View):
    def get(self, request, *args, **kwars):
        try:
            balancete = Balancete.objects.get(id=self.kwargs['id'])

            despesas_valor_total = balancete.despesas.aggregate(
                Sum('saldo'))
            despesas_valor_total = despesas_valor_total['saldo__sum'] or 0

            receitas_valor_total = balancete.receitas.aggregate(
                Sum('saldo'))
            receitas_valor_total = receitas_valor_total['saldo__sum'] or 0

            valor_total = receitas_valor_total - despesas_valor_total

            context = {
                'balancete': balancete,
                'despesas_list': balancete.despesas.all(),
                'despesas_count': balancete.despesas.all().count,
                'despesas_total': despesas_valor_total,
                'receitas_list': balancete.receitas.all(),
                'receitas_count': balancete.receitas.all().count,
                'receitas_total': receitas_valor_total,
                'valor_total': valor_total
            }
        except Balancete.DoesNotExist:
            raise Http404("Balancete não existe")

        return render(request, 'projeto/balancete_detalhado.html', context)


class CadastrarDespesaView(generic.View):
    def get(self, request, *args, **kwargs):
        form = DespesaForm()

        return render(request, 'projeto/cadastrar_despesa.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = DespesaForm(request.POST)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            saldo = form.cleaned_data['saldo']

            despesa = Despesa(titulo=titulo, saldo=saldo)
            despesa.save()

            balancete_do_mes = Balancete.objects.get(
                usuario=request.user,
                referencia=f"{timezone.now().month}_{timezone.now().year}"
            )
            balancete_do_mes.despesas.add(despesa)

            return HttpResponseRedirect('/')


class CadastrarReceitaView(generic.View):
    def get(self, request, *args, **kwargs):
        form = ReceitaForm()

        return render(request, 'projeto/cadastrar_receita.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ReceitaForm(request.POST)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            saldo = form.cleaned_data['saldo']

            receita = Receita(titulo=titulo, saldo=saldo)
            receita.save()

            balancete_do_mes = Balancete.objects.get(
                usuario=request.user,
                referencia=f"{timezone.now().month}_{timezone.now().year}"
            )
            balancete_do_mes.receitas.add(receita)

            return HttpResponseRedirect('/')


class CriarBalancete(generic.View):
    def post(self, request, *args, **kwargs):
        balancete = Balancete(usuario=request.user)
        balancete.save()

        return HttpResponseRedirect('/')


class CadastrarUsuarioView(generic.View):
    def get(self, request, *args, **kwargs):
        form = UsuarioForm()

        return render(request, 'projeto/cadastrar_usuario.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            senha = form.cleaned_data['senha']

            usuario = User.objects.create_user(nome, None, senha)
            usuario.save()

            return HttpResponseRedirect('/')


class LoginUsuarioView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, "projeto/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST['nome']
        password = request.POST['senha']

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)

            return HttpResponseRedirect('/')
        else:
            return render(request, "projeto/login.html", {'error_msg': "Nome de usuário ou senha está incorreto"})


class LogoutUsuarioView(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect('/login')
