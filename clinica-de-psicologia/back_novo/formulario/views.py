from django.http import JsonResponse
from django.shortcuts import render
from .forms import InscritoComunidadeForm
import json

def formulario_comunidade_view(request):
    
    # A view 'GET' apenas renderiza o seu template HTML
    if request.method == 'GET':
        # Não precisamos passar o 'form' aqui, já que seu HTML
        # renderiza os campos manualmente.
        return render(request, 'formulario/comunidade_form.html')

    # A view 'POST' é o que seu JavaScript chama via 'fetch'
    if request.method == 'POST':
        try:
            # O JS envia JSON, então lemos o 'request.body'
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido.'}, status=400)

        # --- Mapeamento de Nomes ---
        # Seu JS envia nomes com underline (ex: nome_inscrito)
        # Seu ModelForm espera nomes sem underline (ex: nomeinscrito)
        # Vamos traduzir os nomes aqui.
        
        mapped_data = {} # Usaremos um novo dict para evitar problemas
        
        # Mapeia os nomes do JS para os nomes do ModelForm
        mapped_data['nomeinscrito'] = data.get('nome_inscrito')
        mapped_data['dtnascimento'] = data.get('data_nascimento')
        mapped_data['cpfinscrito'] = data.get('cpf_inscrito')
        mapped_data['tellcellinscrito'] = data.get('telefone_inscrito')
        mapped_data['emailinscrito'] = data.get('email_inscrito')
        mapped_data['identidadegenero'] = data.get('identidade_genero')
        mapped_data['etnia'] = data.get('cor_etnia')
        mapped_data['religiao'] = data.get('religiao') # Nomes já batem
        mapped_data['estadocivilinscrito'] = data.get('estado_civil_inscrito')
        mapped_data['confirmlgpd'] = data.get('deAcordo', False)

        # Endereço (Nomes já batem)
        mapped_data['rua'] = data.get('rua')
        mapped_data['bairro'] = data.get('bairro')
        mapped_data['cidade'] = data.get('cidade')
        mapped_data['uf'] = data.get('uf')
        mapped_data['cep'] = data.get('cep')
        
        # Responsável (se houver)
        if data.get('menorIdade', False): # Checa se o checkbox 'menorIdade' foi marcado
            mapped_data['nomeresp'] = data.get('nome_responsavel')
            mapped_data['cpfresp'] = data.get('cpf_responsavel')
            mapped_data['tellcellresp'] = data.get('telefone_responsavel')
            mapped_data['emailresp'] = data.get('email_responsavel')
            mapped_data['estadocivilresp'] = data.get('estado_civil_responsavel')
            mapped_data['grauresp'] = data.get('parentesco_responsavel')

        # Contato de Urgência (pegando apenas o primeiro)
        # O seu JS envia 'nome_urgencia[]' como uma lista
        nome_urgencia_list = data.get('nome_urgencia[]', [])
        mapped_data['nomecontatourgencia'] = nome_urgencia_list[0] if nome_urgencia_list else None
        
        telefone_urgencia_list = data.get('telefone_urgencia[]', [])
        mapped_data['contatourgencia'] = telefone_urgencia_list[0] if telefone_urgencia_list else None
        
        # Mapeia os campos multi-select do JS (que são 'ansiedade,luto')
        # para os nomes de campo do Django
        mapped_data['motivos_acompanhamento'] = data.get('motivos_acompanhamento')
        mapped_data['medicamentos_usados'] = data.get('medicamentos_usados')
        mapped_data['pcd_neurodivergente'] = data.get('pcd_neurodivergente')
        mapped_data['doencas_fisicas'] = data.get('doencas_fisicas')
        
        # Mapeia os nomes dos campos que não batem
        mapped_data['tipo_terapias'] = data.get('tipo_terapias')
        mapped_data['disponibilidade_semana'] = data.get('disponibilidade')

        # Passa o dicionário 'mapped_data' limpo para o formulário
        form = InscritoComunidadeForm(mapped_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Inscrição realizada com sucesso!'})
        else:
            # Retorna os erros de validação para o seu JS
            # Seu JS espera os nomes dos campos do HTML, então precisamos
            # mapear os erros de volta (ex: 'nomeinscrito' -> 'nome_inscrito')
            erros_mapeados = {}
            for field, messages in form.errors.items():
                if field == 'nomeinscrito': erros_mapeados['nome_inscrito'] = messages
                elif field == 'dtnascimento': erros_mapeados['data_nascimento'] = messages
                elif field == 'cpfinscrito': erros_mapeados['cpf_inscrito'] = messages
                elif field == 'tellcellinscrito': erros_mapeados['telefone_inscrito'] = messages
                elif field == 'emailinscrito': erros_mapeados['email_inscrito'] = messages
                elif field == 'identidadegenero': erros_mapeados['identidade_genero'] = messages
                elif field == 'etnia': erros_mapeados['cor_etnia'] = messages
                elif field == 'estadocivilinscrito': erros_mapeados['estado_civil_inscrito'] = messages
                elif field == 'confirmlgpd': erros_mapeados['deAcordo'] = messages
                elif field == 'nomeresp': erros_mapeados['nome_responsavel'] = messages
                elif field == 'cpfresp': erros_mapeados['cpf_responsavel'] = messages
                elif field == 'tellcellresp': erros_mapeados['telefone_responsavel'] = messages
                elif field == 'emailresp': erros_mapeados['email_responsavel'] = messages
                elif field == 'estadocivilresp': erros_mapeados['estado_civil_responsavel'] = messages
                elif field == 'grauresp': erros_mapeados['parentesco_responsavel'] = messages
                elif field == 'nomecontatourgencia': erros_mapeados['nome_urgencia[]'] = messages
                elif field == 'contatourgencia': erros_mapeados['telefone_urgencia[]'] = messages
                elif field == 'motivos_acompanhamento': erros_mapeados['motivos_acompanhamento_display'] = messages
                elif field == 'medicamentos_usados': erros_mapeados['medicamentos_usados_display'] = messages
                elif field == 'pcd_neurodivergente': erros_mapeados['pcd_neurodivergente_display'] = messages
                elif field == 'doencas_fisicas': erros_mapeados['doencas_fisicas_display'] = messages
                elif field == 'tipo_terapias': erros_mapeados['tipo_terapias_display'] = messages
                elif field == 'disponibilidade_semana': erros_mapeados['disponibilidade_display'] = messages
                else: erros_mapeados[field] = messages

            return JsonResponse({'status': 'erro_validacao', 'erros': erros_mapeados}, status=400)

    # Se for outro método (PUT, etc.)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido.'}, status=405)

