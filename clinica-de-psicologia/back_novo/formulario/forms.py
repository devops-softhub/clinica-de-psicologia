from django import forms
from .models import (
    Disponibilidade, Doencafisica, Endereco, Inscritocomunidade, 
    Inscritoconvenio, Medicamento, Motivoacompanhamento, Pcdsnd, Tipoterapia
)

# --- INÍCIO: DEFINIÇÃO DOS CHOICES --- 

# (Mantidos do seu forms.py original, pois são usados pelo ModelForm e validação)
ESTADO_CIVIL_CHOICES = [
    ('Solteiro', 'Solteiro'), ('Casado', 'Casado'), ('Divorciado', 'Divorciado'),
    ('Viúvo', 'Viúvo'), ('União Estável', 'União Estável'), ('Nenhum', 'Nenhum'), ('Outros', 'Outros'),
] 
GENERO_CHOICES = [
    ('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Não Binário', 'Não Binário'),
    ('Transgênero', 'Transgênero'), ('Outros', 'Outros'), ('pref-nao-dizer', 'Prefiro não dizer'),
] 
ETNIA_CHOICES = [
    ('Branca', 'Branca'), ('Preta', 'Preta'), ('Parda', 'Parda'),
    ('Amarela', 'Amarela'), ('Indígena', 'Indígena'), ('Outra', 'Outra'), # 'Outras' -> 'Outra'
] 
RELIGIAO_CHOICES = [
    ('Católica', 'Católica'), ('Evangélica', 'Evangélica'), ('Budismo', 'Budismo'),
    ('Espirita', 'Espirita'), ('Hinduísmo', 'Hinduísmo'), ('Islamismo', 'Islamismo'),
    ('Judaismo', 'Judaismo'), ('Religião de Matriz Africana', 'Religião de Matriz Africana'),
    ('Outra', 'Outra'), ('Nenhuma', 'Nenhuma / Agnóstico / Ateu'),
]
MOTIVOS_CHOICES = [
    ('ansiedade', 'Ansiedade'), ('assediomoral', 'Assédio Moral'), ('depressao', 'Depressão'),
    ('dfaprendizagem', 'Dificuldade de Aprendizagem'), ('humorinstavel', 'Humor Instável'),
    ('insonia', 'Insônia'), ('isolasocial', 'Isolamento Social'), ('luto', 'Luto'),
    ('tristeza', 'Tristeza'), ('apatia', 'Apatia'), ('chorofc', 'Choro Frequente'),
    ('exaustao', 'Exaustão'), ('fadiga', 'Fadiga'), ('faltanimo', 'Falta de Ânimo'),
    ('vldt', 'Vazio/Invalidez'), ('assediosexual', 'Assédio Sexual'), ('outro', 'Outro')
] 
DOENCAS_CHOICES = [
    ('doencaresp', 'Doença Respiratória'), ('cancer', 'Câncer'), ('diabete', 'Diabetes'),
    ('disfusexual', 'Disfunção Sexual'), ('doencadgt', 'Doença Digestiva'), 
    ('escleorosemlt', 'Esclerose Múltipla'), ('hcpt', 'Hipertensão'), ('luposatm', 'Lúpus'), 
    ('obesidade', 'Obesidade'), ('pblmarenal', 'Problema Renal'), ('outro', 'Outro'), ('nenhum', 'Nenhum')
] 
PCD_CHOICES = [
    ('tea', 'Autismo (TEA)'), ('tdah', 'TDAH'), ('dffs', 'Disfunção Fonoaudiológica'),
    ('dfv', 'Deficiência Visual'), ('dfa', 'Deficiência Auditiva'), ('ttap', 'Transtorno de Aprendizagem'),
    ('ahst', 'Altas Habilidades/Superdotação'), ('outro', 'Outro'), ('nenhum', 'Nenhum')
] 
MEDICAMENTOS_CHOICES = [
    ('ansiolitico', 'Ansiolítico'), ('antidepressivo', 'Antidepressivo'),
    ('antipsicotico', 'Antipsicótico'), ('estabhumor', 'Estabilizador de Humor'),
    ('memoriatct', 'Memória/Concentração'), ('outro', 'Outro'), ('nenhum', 'Nenhum')
]

# --- NOVOS CHOICES (para bater com os <select> do HTML) ---
TERAPIA_CHOICES_HTML = [
    ('individual', 'Individual'),
    ('grupo', 'Grupo'),
    ('casal', 'Casal'),
    ('familia', 'Família'),
]
DISPONIBILIDADE_CHOICES_HTML = [
    ('manha_semana', 'Manhã (Segunda a Sexta)'),
    ('tarde_semana', 'Tarde (Segunda a Sexta)'),
    ('noite_semana', 'Noite (Segunda a Sexta)'),
    ('sabado_manha', 'Sábado (Somente pela manhã, 8:30h às 12h)'),
]

# --- A "PONTE" PARA O JAVASCRIPT ---
# Este campo personalizado converte a string "ansiedade,luto" do JS
# em uma lista ["ansiedade", "luto"] que o Django entende.
class CommaSeparatedMultipleChoiceField(forms.MultipleChoiceField):
    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        # O seu JS envia os dados como uma string separada por vírgula
        # A view.py garante que seja uma string
        return [v for v in value.split(',') if v] # filter(Boolean)

    def validate(self, value):
        # Roda a validação padrão do MultipleChoiceField
        super().validate(value)


class BaseInscritoForm(forms.ModelForm):
    
    # --- Campos de Escolha Única (Dropdowns) ---
    # (Validação para os <select> do HTML)
    estadocivilinscrito = forms.ChoiceField(
        choices=ESTADO_CIVIL_CHOICES, required=True, label="Estado Civil (Inscrito)"
    )
    identidadegenero = forms.ChoiceField(
        choices=GENERO_CHOICES, required=True, label="Identidade de Gênero"
    )
    etnia = forms.ChoiceField(
        choices=ETNIA_CHOICES, required=True, label="Etnia"
    )
    religiao = forms.ChoiceField(
        choices=RELIGIAO_CHOICES, required=True, label="Religião"
    )
    estadocivilresp = forms.ChoiceField(
        choices=ESTADO_CIVIL_CHOICES, required=False, label="Estado Civil (Responsável)"
    ) 
    
    # --- Campos de Múltipla Escolha (do JS) ---
    # (Usam a "ponte" CommaSeparatedMultipleChoiceField)
    motivos_acompanhamento = CommaSeparatedMultipleChoiceField(
        choices=MOTIVOS_CHOICES, 
        label="Motivos da Busca do Tratamento", required=False
    )
    doencas_fisicas = CommaSeparatedMultipleChoiceField(
        choices=DOENCAS_CHOICES, 
        label="Possui alguma doença física?", required=False
    )
    pcd_neurodivergente = CommaSeparatedMultipleChoiceField(
        choices=PCD_CHOICES, 
        label="Possui alguma deficiência ou neurodivergência?", required=False
    )
    medicamentos_usados = CommaSeparatedMultipleChoiceField(
        choices=MEDICAMENTOS_CHOICES, 
        label="Faz uso de algum medicamento psiquiátrico?", required=False
    )
    
    # --- MUDANÇA: Campos de Escolha Única (do HTML) ---
    # (Usam ChoiceField normal, pois o JS não os modifica)
    tipo_terapias = forms.ChoiceField(
        choices=TERAPIA_CHOICES_HTML, 
        label="Qual tipo de terapia você busca?", required=True
    )
    disponibilidade_semana = forms.ChoiceField( 
        choices=DISPONIBILIDADE_CHOICES_HTML, 
        label="Qual sua disponibilidade?", required=True
    )
    
    # --- Campos de Endereço ---
    cidade = forms.CharField(max_length=40, label="Cidade")
    bairro = forms.CharField(max_length=50, required=False, label="Bairro")
    rua = forms.CharField(max_length=100, label="Rua/Avenida")
    uf = forms.CharField(max_length=2, initial='DF', label="UF")
    cep = forms.CharField(max_length=10, label="CEP") # Aumentado para 10 para 'XXXXX-XXX'

    # --- MÉTODO SAVE ATUALIZADO ---
    # Este método agora salva corretamente AMBOS os tipos de campo
    def save(self, commit=True):
        inscrito = super().save(commit=False)
        
        if commit:
            inscrito.save()
            
            fk_data = {self._fk_name: inscrito}

            # 1. Salva os campos de MÚLTIPLA ESCOLHA (do JS)
            def save_multiselect_fields(model, field_name, choices_list):
                obj = model(**fk_data)
                selected_values = self.cleaned_data.get(field_name, [])
                for key, _ in choices_list:
                    setattr(obj, key, key in selected_values)
                obj.save()

            save_multiselect_fields(Motivoacompanhamento, 'motivos_acompanhamento', MOTIVOS_CHOICES)
            save_multiselect_fields(Doencafisica, 'doencas_fisicas', DOENCAS_CHOICES)
            save_multiselect_fields(Pcdsnd, 'pcd_neurodivergente', PCD_CHOICES)
            save_multiselect_fields(Medicamento, 'medicamentos_usados', MEDICAMENTOS_CHOICES)
            
            # 2. Salva os campos de ESCOLHA ÚNICA (do HTML)
            
            # Mapeia o valor do <select> (ex: "manha_semana") para o campo do DB (ex: "manha")
            disp_map = {
                'manha_semana': 'manha',
                'tarde_semana': 'tarde',
                'noite_semana': 'noite',
                'sabado_manha': 'sabado'
            }
            disponibilidade_obj = Disponibilidade(**fk_data)
            selected_disp = self.cleaned_data.get('disponibilidade_semana') # Valor (ex: "manha_semana")
            field_to_set = disp_map.get(selected_disp) # Campo do DB (ex: "manha")
            if field_to_set:
                setattr(disponibilidade_obj, field_to_set, True)
            disponibilidade_obj.save()

            # Mapeia o valor (ex: "individual") para o campo (ex: "individualadto")
            # (Estou supondo que 'individual' -> 'individualadto' (Adulto))
            terapia_map = {
                'individual': 'individualadto', 
                'grupo': 'grupo',
                'casal': 'casal',
                'familia': 'familia'
            }
            terapia_obj = Tipoterapia(**fk_data)
            selected_terapia = self.cleaned_data.get('tipo_terapias') # Valor (ex: "individual")
            field_to_set_terapia = terapia_map.get(selected_terapia) # Campo do DB (ex: "individualadto")
            if field_to_set_terapia:
                setattr(terapia_obj, field_to_set_terapia, True)
            terapia_obj.save()

            # 3. Salva o Endereço
            Endereco.objects.create(
                cidade=self.cleaned_data.get('cidade'),
                bairro=self.cleaned_data.get('bairro'),
                rua=self.cleaned_data.get('rua'),
                uf=self.cleaned_data.get('uf'),
                cep=self.cleaned_data.get('cep'),
                **fk_data
            )
            
        return inscrito
        
    class Meta:
        abstract = True
        exclude = ['dthinscricao', 'status']

#
class InscritoComunidadeForm(BaseInscritoForm):
    _fk_name = 'idfichacomunidade'

    class Meta(BaseInscritoForm.Meta):
        model = Inscritocomunidade
        fields = [
            'nomeinscrito', 'dtnascimento', 'nomeresp', 'grauresp', 'cpfresp',
            'estadocivilresp', 'tellcellresp', 'emailresp', 'estadocivilinscrito',
            'cpfinscrito', 'tellcellinscrito', 'contatourgencia', 'nomecontatourgencia',
            'emailinscrito', 'identidadegenero', 'etnia', 'religiao', 'confirmlgpd'
        ]
class InscritoConvenioForm(BaseInscritoForm):
    _fk_name = 'idfichaconvenio'

    class Meta(BaseInscritoForm.Meta):
        model = Inscritoconvenio
        fields = [
            'nomeinscrito', 'dtnascimento', 'testavpsico', 'tipoencaminhamento',
            'nomeresp', 'grauresp', 'cpfresp', 'estadocivilresp', 'tellcellresp',
            'emailresp', 'estadocivilinscrito', 'cpfinscrito', 'tellcellinscrito',
            'contatourgencia', 'emailinscrito', 'identidadegenero', 'etnia',
            'religiao', 'confirmlgpd'
        ]

