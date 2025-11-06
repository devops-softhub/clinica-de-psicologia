from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone 
import datetime
import re
from validate_docbr import CPF
from .models import (
    Disponibilidade, Doencafisica, Endereco, Inscritocomunidade, 
    Inscritoconvenio, Medicamento, Motivoacompanhamento, Pcdsnd, Tipoterapia
)

# --- A "PONTE" PARA O JAVASCRIPT ---
class CommaSeparatedMultipleChoiceField(forms.MultipleChoiceField):
    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return [v for v in value.split(',') if v]

    def validate(self, value):
        super().validate(value)


ESTADO_CIVIL_CHOICES = [
    ('Solteiro', 'Solteiro'), ('Casado', 'Casado'), ('Divorciado', 'Divorciado'),
    ('Viuvo', 'Viúvo'), ('uniao-estavel', 'uniao-estavel'), ('Nenhum', 'Nenhum'), ('Outros', 'Outros'),
] 
GENERO_CHOICES = [
    ('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Nao Binario', 'Não Binário'),
    ('Transgenero', 'Transgênero'), ('Outros', 'Outros'), ('pref-nao-dizer', 'Prefiro não dizer'),
] 
ETNIA_CHOICES = [
    ('Branca', 'Branca'), ('Preta', 'Preta'), ('Parda', 'Parda'),
    ('Amarela', 'Amarela'), ('Indigena', 'Indígena'), ('Outra', 'Outra'),
] 
RELIGIAO_CHOICES = [
    ('Catolica', 'Católica'), ('Evangelica', 'Evangélica'),('Budismo', 'Budismo'),
    ('Espirita', 'Espírita'), ('Hinduismo', 'Hinduísmo'),('Islamismo', 'Islamismo'),
    ('Judaismo', 'Judaísmo'),('Matriz-afro', 'Religião de Matriz Africana'),('Outra', 'Outra'),
    ('Nenhuma', 'Nenhuma / Agnóstico / Ateu'), 
]
# Este é novo, para o convenio.html (usando os values de lá)
ENCAMINHAMENTO_CHOICES = [
    ('caps', 'CAPS - Centro de Atenção Psicossocial'),
    ('cras', 'CRAS - Centro de Referência de Assistência Social'),
    ('creas', 'CREAS - Centro de Referência Especializado de Assistência Social'),
    ('deam', 'DEAM - Delegacia da Mulher'),
    ('dpdf', 'DPDF - Defensoria Pública do Distrito Federal'),
    ('mpdft', 'MPDFT - Ministério Público do Distrito Federal'),
    ('ses', 'SES - Secretaria de Saúde'),
    ('sejus', 'SEJUS - Secretaria de Justiça'),
    ('ubs', 'UBS - Unidade Básica de Saúde'),
    ('clinica_ana_lucia', 'Clínica Ana Lucia Chaves Fecury (Unieuro Asa Sul)'),
    ('outros', 'Outros'),
]

# (CHOICES comuns que já usam minúsculas)
MOTIVOS_CHOICES = [
    ('ansiedade', 'Ansiedade'), ('assediomoral', 'Assédio Moral'), ('depressao', 'Depressão'),
    ('dfaprendizagem', 'Dificuldade de Aprendizagem'), ('humorinstavel', 'Humor Instável'),
    ('insonia', 'Insônia'), ('isolasocial', 'Isolamento Social'), ('luto', 'Luto'),
    ('tristeza', 'Tristeza'), ('apatia', 'Apatia'), ('chorofc', 'Choro Frequente'),
    ('exaustao', 'Exaustão'), ('fadiga', 'Fadiga'), ('faltanimo', 'Falta de Ânimo'),
    ('vldt', 'Vazio/Invalidez'), ('assediosexual', 'Assédio Sexual'), ('outro', 'Outro')
] 
DOENCAS_CHOICES = [
    ('doencaresp', 'Doença Respiratória'),('cancer', 'Câncer'),('diabete', 'Diabetes'),
    ('disfusexual', 'Disfunção Sexual'),('doencadgt', 'Doença Digestiva'),('escleorosemlt', 'Esclerose Múltipla'),
    ('hcpt', 'Hipertensão'),('luposatm', 'Lúpus'),('obesidade', 'Obesidade'),
    ('pblmarenal', 'Problema Renal'),('outro', 'Outro'),('nenhum', 'Nenhum')
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
TERAPIA_CHOICES_HTML = [
    ('individual', 'Individual'), ('grupo', 'Grupo'),
    ('casal', 'Casal'), ('familia', 'Família'),
]
DISPONIBILIDADE_CHOICES_HTML = [
    ('manha_semana', 'Manhã (Segunda a Sexta)'), ('tarde_semana', 'Tarde (Segunda a Sexta)'),
    ('noite_semana', 'Noite (Segunda a Sexta)'), ('sabado_manha', 'Sábado (Somente pela manhã, 8:30h às 12h)'),
]

# =======================================================================
# --- FORMULÁRIO BASE UNIVERSAL (Como você sugeriu) ---
# =======================================================================

class BaseInscritoForm(forms.ModelForm):
    
    # --- CAMPOS COMUNS (Agora herdados por todos) ---
    estadocivilinscrito = forms.ChoiceField(
        choices=ESTADO_CIVIL_CHOICES, required=True
    )
    identidadegenero = forms.ChoiceField(
        choices=GENERO_CHOICES, required=True
    )
    etnia = forms.ChoiceField(
        choices=ETNIA_CHOICES, required=True
    )
    religiao = forms.ChoiceField(
        choices=RELIGIAO_CHOICES, required=True
    )
    estadocivilresp = forms.ChoiceField(
        choices=ESTADO_CIVIL_CHOICES, required=False
    ) 
    motivos_acompanhamento = CommaSeparatedMultipleChoiceField(
        choices=MOTIVOS_CHOICES, required=False
    )
    doencas_fisicas = CommaSeparatedMultipleChoiceField(
        choices=DOENCAS_CHOICES, required=False
    )
    pcd_neurodivergente = CommaSeparatedMultipleChoiceField(
        choices=PCD_CHOICES, required=False
    )
    medicamentos_usados = CommaSeparatedMultipleChoiceField(
        choices=MEDICAMENTOS_CHOICES, required=False
    )
    tipo_terapias = forms.ChoiceField(
        choices=TERAPIA_CHOICES_HTML, required=True
    )
    disponibilidade_semana = forms.ChoiceField( 
        choices=DISPONIBILIDADE_CHOICES_HTML, required=True
    )
    cidade = forms.CharField(max_length=40, label="Cidade")
    bairro = forms.CharField(max_length=50, required=False, label="Bairro")
    rua = forms.CharField(max_length=100, label="Rua/Avenida")
    uf = forms.CharField(max_length=2, initial='DF', label="UF")
    cep = forms.CharField(max_length=9, label="CEP") # Alinhado com XXXXX-XXX

    # --- MÉTODO SAVE (Comum) ---
    def save(self, commit=True):
        inscrito = super().save(commit=False)
        
        if commit:
            inscrito.save()
            fk_data = {self._fk_name: inscrito}

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
            
            disp_map = {
                'manha_semana': 'manha', 'tarde_semana': 'tarde',
                'noite_semana': 'noite', 'sabado_manha': 'sabado'
            }
            disponibilidade_obj = Disponibilidade(**fk_data)
            selected_disp = self.cleaned_data.get('disponibilidade_semana') 
            field_to_set = disp_map.get(selected_disp)
            if field_to_set:
                setattr(disponibilidade_obj, field_to_set, True)
            disponibilidade_obj.save()

            terapia_map = {
                'individual': 'individualadto', 'grupo': 'grupo',
                'casal': 'casal', 'familia': 'familia'
            }
            terapia_obj = Tipoterapia(**fk_data)
            selected_terapia = self.cleaned_data.get('tipo_terapias')
            field_to_set_terapia = terapia_map.get(selected_terapia)
            if field_to_set_terapia:
                setattr(terapia_obj, field_to_set_terapia, True)
            terapia_obj.save()

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

    # --- MÉTODOS DE VALIDAÇÃO (Comuns) ---
    def clean_dtnascimento(self):
        data_nascimento = self.cleaned_data.get('dtnascimento')
        if data_nascimento:
            today = timezone.now().date()
            if data_nascimento > today:
                raise ValidationError('A data de nascimento não pode ser no futuro.')
            if data_nascimento.year < 1899:
                raise ValidationError('O ano não pode ser anterior a 1899.')
        return data_nascimento

    def clean_cpfinscrito(self):
        cpf_str = self.cleaned_data.get('cpfinscrito')
        if cpf_str:
            cpf_validator = CPF()
            if not cpf_validator.validate(cpf_str):
                raise ValidationError('CPF inválido. Verifique os dígitos.')
        # Salva com máscara (requer max_length=14 no model)
        return cpf_str 

    def clean_cpfresp(self):
        cpf_str = self.cleaned_data.get('cpfresp')
        if cpf_str:
            cpf_validator = CPF()
            if not cpf_validator.validate(cpf_str):
                raise ValidationError('CPF do responsável inválido. Verifique os dígitos.')
        # Salva com máscara (requer max_length=14 no model)
        return cpf_str 

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            if not re.fullmatch(r'\d{5}-\d{3}', cep):
                raise ValidationError('Formato de CEP inválido. O formato esperado é XXXXX-XXX')
        return cep


class InscritoComunidadeForm(BaseInscritoForm):
    _fk_name = 'idfichacomunidade'

    class Meta(BaseInscritoForm.Meta):
        model = Inscritocomunidade
        # Lista APENAS os campos do model que NÃO estão na BaseInscritoForm
        fields = [
            'nomeinscrito', 'dtnascimento', 'nomeresp', 'grauresp', 'cpfresp',
            'tellcellresp', 'emailresp', 'cpfinscrito', 'tellcellinscrito', 
            'contatourgencia', 'nomecontatourgencia', 'emailinscrito', 'confirmlgpd'
        ]

class InscritoConvenioForm(BaseInscritoForm):
    _fk_name = 'idfichaconvenio'

    # Campo ADICIONAL que só existe no Convênio
    tipoencaminhamento = forms.ChoiceField(
        choices=ENCAMINHAMENTO_CHOICES, required=True
    )

    class Meta(BaseInscritoForm.Meta):
        model = Inscritoconvenio

        fields = [
            'nomeinscrito', 'dtnascimento', 
            'nomeresp', 'grauresp', 'cpfresp', 'tellcellresp',
            'emailresp', 'cpfinscrito', 'tellcellinscrito',
            'emailinscrito', 'confirmlgpd'
        ]
