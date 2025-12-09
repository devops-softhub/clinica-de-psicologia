from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from formulario.models import Inscritocomunidade
from datetime import date

@login_required
def dashboard_estagiario(request):
    """
    Dashboard principal do Estagiário.
    Exibe seus pacientes vinculados e atendimentos da semana.
    """
    
    # TODO: Implementar lógica real de vinculação (Estagiario -> Paciente)
    # Atualmente não há um modelo de 'Vinculo' ou 'Prontuario' claro no código fornecido.
    # Estamos listando os últimos inscritos da comunidade como placeholder.
    inscritos = Inscritocomunidade.objects.order_by('-dthinscricao')[:3]
    
    # Mock de atendimentos para visualização (já que não há modelo de Agendamento/Atendimento)
    atendimentos = [
        {
            'paciente_nome': 'Maria Silva', 
            'status': 'Pendente', 
            'data': date(2025, 5, 14), 
            'acao_label': 'Aberto'
        },
        {
            'paciente_nome': 'Rafael Costa', 
            'status': 'Atendido', 
            'data': date(2025, 6, 10), 
            'acao_label': 'Fechado'
        },
    ]

    context = {
        'inscritos': inscritos,
        'atendimentos': atendimentos,
    }
    return render(request, 'DashboardEstagiario.html', context)
