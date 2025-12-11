from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from usuarios.models import Usuario
from coodernador.models import Prontuario

class SupervisorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.cargo == 'SUPER'

from django.views import View
from formulario.models import Inscritocomunidade, Inscritoconvenio
from django.contrib import messages

class SupervisorOrRTRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.cargo in ['SUPER', 'RESP_TEC']

class DashboardSupervisorView(LoginRequiredMixin, SupervisorRequiredMixin, ListView):
    model = Usuario
    template_name = 'dashboard_supervisor.html'
    context_object_name = 'estagiarios'

    def get_queryset(self):
        # Get interns linked to this supervisor
        return Usuario.objects.filter(
            supervisor_vinculado=self.request.user,
            cargo='ESTAG'
        ).annotate(
            num_pacientes=Count('prontuarios_estagiario', filter=Q(prontuarios_estagiario__status_ativo=True))
        )

class EstagiarioDetailView(LoginRequiredMixin, SupervisorOrRTRequiredMixin, DetailView):
    model = Usuario
    template_name = 'estagiario_detail.html'
    context_object_name = 'estagiario'

    def get_queryset(self):
        # RT can see any intern, Supervisor only their own
        if self.request.user.cargo == 'RESP_TEC':
            return Usuario.objects.filter(cargo='ESTAG')
        return Usuario.objects.filter(supervisor_vinculado=self.request.user, cargo='ESTAG')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prontuarios'] = Prontuario.objects.filter(estagiario=self.object, status_ativo=True).select_related('paciente_comunidade', 'paciente_convenio')
        return context

class FinalizarCicloView(LoginRequiredMixin, SupervisorOrRTRequiredMixin, View):
    def post(self, request, pk):
        prontuario = get_object_or_404(Prontuario, pk=pk)
        
        # TODO: Implement PDF generation and saving logic here
        # For now, we just close the Prontuario
        
        prontuario.status_ativo = False
        prontuario.save()
        
        messages.success(request, "Ciclo finalizado com sucesso. Prontuário arquivado.")
        
        # Redirect back to dashboard or intern detail
        if request.user.cargo == 'RESP_TEC':
            return redirect('resptecn:dashboard')
        return redirect('supervisor:dashboard')

class DesvincularDevolverView(LoginRequiredMixin, SupervisorOrRTRequiredMixin, View):
    def post(self, request, pk):
        prontuario = get_object_or_404(Prontuario, pk=pk)
        
        # Close current Prontuario to release the patient
        prontuario.status_ativo = False
        prontuario.save()
        
        messages.success(request, "Inscrito desvinculado e devolvido à lista de espera.")
        
        if request.user.cargo == 'RESP_TEC':
            return redirect('resptecn:dashboard')
        return redirect('supervisor:dashboard')

class VincularInscritoView(LoginRequiredMixin, SupervisorOrRTRequiredMixin, View):
    def get(self, request, tipo, pk):
        # This view should render a form to select an intern to link to the patient
        # For simplicity, let's assume we list interns and let user pick one
        
        if tipo == 'comunidade':
            paciente = get_object_or_404(Inscritocomunidade, pk=pk)
        else:
            paciente = get_object_or_404(Inscritoconvenio, pk=pk)
            
        # List interns available for this supervisor (or all if RT)
        if request.user.cargo == 'RESP_TEC':
            estagiarios = Usuario.objects.filter(cargo='ESTAG', is_active=True)
        else:
            estagiarios = Usuario.objects.filter(cargo='ESTAG', supervisor_vinculado=request.user, is_active=True)
            
        return render(request, 'vincular_inscrito.html', {
            'paciente': paciente,
            'tipo': tipo,
            'estagiarios': estagiarios
        })

    def post(self, request, tipo, pk):
        estagiario_id = request.POST.get('estagiario')
        estagiario = get_object_or_404(Usuario, pk=estagiario_id)
        
        if tipo == 'comunidade':
            paciente_comunidade = get_object_or_404(Inscritocomunidade, pk=pk)
            paciente_convenio = None
        else:
            paciente_comunidade = None
            paciente_convenio = get_object_or_404(Inscritoconvenio, pk=pk)
            
        # Create Prontuario
        # We need a Coordenador and Supervisor for the Prontuario.
        # If user is Supervisor, use them. If RT, maybe use the intern's supervisor?
        
        supervisor = estagiario.supervisor_vinculado
        if not supervisor:
             messages.error(request, "O estagiário selecionado não possui supervisor vinculado.")
             return redirect('supervisor:vincular_inscrito', tipo=tipo, pk=pk)

        # We need a Coordenador. Prontuario model requires it.
        # We might need to fetch a default coordinator or the current user if they are coord (but they are Super/RT).
        # Let's find the first active Coordenador.
        coordenador = Usuario.objects.filter(cargo='COORD', is_active=True).first()
        if not coordenador:
             # Fallback if no coordinator exists (should not happen in prod)
             coordenador = request.user 
        
        Prontuario.objects.create(
            estagiario=estagiario,
            supervisor=supervisor,
            coordenador=coordenador,
            paciente_comunidade=paciente_comunidade,
            paciente_convenio=paciente_convenio,
            status_ativo=True
        )
        
        messages.success(request, "Inscrito vinculado com sucesso!")
        if request.user.cargo == 'RESP_TEC':
            return redirect('resptecn:dashboard')
        return redirect('supervisor:dashboard')

