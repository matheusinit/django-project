from django.urls import path
from . import views

app_name = "projeto"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('receitas', views.MostrarReceitasView.as_view(), name='mostrar_receitas'),
    path('despesas', views.MostrarDespesasView.as_view(), name='mostrar_despesas'),
    path('cadastrar/receita', views.CadastrarReceitaView.as_view(),
         name='criar_receita'),
    path('cadastrar/despesa', views.CadastrarDespesaView.as_view(),
         name='criar_despesa'),
    path('cadastrar', views.CadastrarUsuarioView.as_view(),
         name='cadastrar_usuario'),
    path('login', views.LoginUsuarioView.as_view(), name='login_usuario'),
    path('logout', views.LogoutUsuarioView.as_view(), name='logout_usuario'),
    path('criar/balancete', views.CriarBalancete.as_view(), name='criar_balancete'),
    path('balancetes', views.MostrarBalancetesView.as_view(),
         name='mostrar_balancetes'),
    path('balancete/<int:id>', views.MostrarBalanceteView.as_view(),
         name='mostrar_balancete')
]
