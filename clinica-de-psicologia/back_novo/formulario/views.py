from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def comunidade(request):
    if request.method == "GET":
        return render(request, 'formulario/comunidade_form.html')
    try:
        dados_inscrito = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status':'erro', 'mensagem':'Json invàlido'}, status=400)
    mapa_nomes = {
        'nome_inscrito': 'nomeinscrito',
        'data_nascimento': 'dtnascimento',
        'nome_responsavel': 'nomeresp',
        'parentesco_responsavel': 'grauresp',
        'cpf_responsavel': 'cpfresp',
        'estado_civil_responsavel': 'estadocivilresp',
        'telefone_responsavel': 'tellcellresp',
        'email_responsavel': 'emailresp',
        'estado_civil_inscrito': 'estadocivilinscrito',
        'cpf_inscrito': 'cpfinscrito',
        'telefone_inscrito': 'tellcellinscrito',
        'nome_urgencia': 'nomecontatourgencia',
        'telefone_urgencia': 'contatourgencia',
        'email_inscrito': 'emailinscrito',
        'identidade_genero': 'identidadegenero',
        'cor_etnia': 'etnia',
        'deAcordo': 'confirmlgpd'
    }

    dados_django= {}
    for nome_html, nome_model in mapa_nomes.itens():
        if nome_html in dados_inscrito:
            dados_django[nome_model] = dados_inscrito[nome_html]
    
    for key, value in dados_inscrito.itens():
        if key not in mapa_nomes:
            dados_django[key] = value

    campos_multiplos = {
        'motivo_busca': 'motivos_acompanhamento',
        'doencas_fisicas': 'doencas_fisicas',
        'disponibilidade': 'disponibilidade_semana',
        'pcd_neurodivergencia': 'pcd_neurodivergente',
        'tipo_terapia': 'tipo_terapias',
        'uso_medicacao': 'medicamentos_usados' # Assumindo que este também é múltiplo
    }

    for nome_html, nome_form in campos_multiplos.items():
        if nome_html in dados_frontend and dados_frontend[nome_html]:
            dados_django[nome_form] = [dados_frontend[nome_html]]
        else:
            dados_django[nome_form] = []

    form = InscritoComunidadeForm(dados_django)

    if form.is_valid():
        try:
            # Chama o seu método save() personalizado que já cuida de tudo!
            form.save()
            return JsonResponse({
                'status': 'sucesso', 
                'mensagem': 'Inscrição realizada com sucesso!'
            }, status=201)
        except Exception as e:
            return JsonResponse({'status': 'erro_servidor', 'mensagem': str(e)}, status=500)
    else:
        return JsonResponse({
            'status': 'erro_validacao',
            'erros': form.errors
        }, status=400)

def convenio(request):
    return render(request, 'formulario/convenio_form.html')