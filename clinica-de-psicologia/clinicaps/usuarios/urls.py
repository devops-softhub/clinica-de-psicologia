from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    # Login e Logout
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('redirect/', views.redirect_after_login, name='redirect_dashboard'),
    path('cadastro/', views.CadastroUsuarioView.as_view(), name='cadastro_usuario'),
    path('dashboard/coord/', views.DashboardCoordenadorView.as_view(), name='dash_coord'),
    path('usuarios/editar/<int:pk>/', views.EditarUsuarioView.as_view(), name='editar_usuario'),
    path('usuarios/deletar/<int:pk>/', views.DeletarUsuarioView.as_view(), name='deletar_usuario'),
    path('nova-senha/', views.NovaSenhaView.as_view(), name='nova_senha'),
    path('verificar-codigo/', views.VerificarCodigoView.as_view(), name='verificar_codigo'),
]