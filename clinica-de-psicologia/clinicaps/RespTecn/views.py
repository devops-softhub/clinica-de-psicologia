from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from usuarios.models import Usuario
from coodernador.models import Prontuario

class RespTecnRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.cargo == 'RESP_TEC'

class DashboardRespTecnView(LoginRequiredMixin, RespTecnRequiredMixin, ListView):
    model = Prontuario
    template_name = 'dashboard_resptecn.html'
    context_object_name = 'prontuarios'
    paginate_by = 20

    def get_queryset(self):
        queryset = Prontuario.objects.filter(status_ativo=True).select_related(
            'estagiario', 
            'estagiario__supervisor_vinculado',
            'paciente_comunidade', 
            'paciente_convenio'
        )
        
        # Filtros
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(paciente_comunidade__nomeinscrito__icontains=search) |
                Q(paciente_convenio__nomeinscrito__icontains=search) |
                Q(estagiario__nome_completo__icontains=search)
            )
            
        return queryset

class ListaSupervisoresView(LoginRequiredMixin, RespTecnRequiredMixin, ListView):
    model = Usuario
    template_name = 'lista_supervisores.html'
    context_object_name = 'supervisores'

    def get_queryset(self):
        return Usuario.objects.filter(cargo='SUPER').annotate(
            num_estagiarios=Count('estagiarios_supervisionados')
        )

class SupervisorDetailView(LoginRequiredMixin, RespTecnRequiredMixin, DetailView):
    model = Usuario
    template_name = 'supervisor_detail_rt.html'
    context_object_name = 'supervisor'

    def get_queryset(self):
        return Usuario.objects.filter(cargo='SUPER')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estagiarios'] = Usuario.objects.filter(
            supervisor_vinculado=self.object, 
            cargo='ESTAG'
        ).annotate(
            num_pacientes=Count('prontuarios_estagiario', filter=Q(prontuarios_estagiario__status_ativo=True))
        )
        return context
