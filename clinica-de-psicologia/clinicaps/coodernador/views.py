from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from usuarios.models import Usuario

# --- MIXINS ---
class CoordenadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.cargo == 'COORD' or self.request.user.is_superuser)

    def handle_no_permission(self):
        return redirect('redirect_dashboard') # Redireciona para uma home genérica ou login

# --- VIEWS ---

# @login_required
# def dashboard_home(request):
#     """
#     View principal que redireciona para o dashboard específico do cargo.
#     """
#     user = request.user
#     if user.cargo == 'COORD':
#         return redirect('coodernador:coord')
#     elif user.cargo == 'SUPER':
#         return redirect('coodernador:supervisor')
#     elif user.cargo == 'ESTAG':
#         return redirect('estagiario:home')
    
#     return render(request, 'dashboard_coord.html') # Fallback

class DashboardCoordenadorView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Usuario
    template_name = 'dashboard_coord.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return Usuario.objects.filter(is_active=True).exclude(id=self.request.user.id).order_by('-dth_insert')

@login_required
def dashboard_estagiario(request):
    return render(request, 'dashboard.html', {'role': 'Estagiário'})

@login_required
def dashboard_supervisor(request):
    return render(request, 'dashboard.html', {'role': 'Supervisor'})

# --- VIEWS ---

@login_required
def dashboard_home(request):
    """
    View principal que redireciona para o dashboard específico do cargo.
    """
    user = request.user
    if user.cargo == 'COORD':
        return redirect('coodernador:coord')
    elif user.cargo == 'SUPER':
        return redirect('coodernador:supervisor')
    elif user.cargo == 'ESTAG':
        return redirect('coodernador:estagiario')
    
    return render(request, 'dashboard.html') # Fallback

class DashboardCoordenadorView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Usuario
    template_name = 'dashboard_coord.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return Usuario.objects.filter(is_active=True).exclude(id=self.request.user.id).order_by('-dth_insert')

@login_required
def dashboard_estagiario(request):
    return render(request, 'dashboard.html', {'role': 'Estagiário'})

@login_required
def dashboard_supervisor(request):
    return render(request, 'dashboard.html', {'role': 'Supervisor'})