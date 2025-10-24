from django import forms
from .models import (
    Disponibilidade, Doencafisica, Endereco, Inscritocomunidade, 
    Inscritoconvenio, Medicamento, Motivoacompanhamento, Pcdsnd, Tipoterapia
)

# A classe BaseInstritoform serve como base para 2 forms filhas que vão ser feitas com base no models incritoconvenio e inscritocomunidade
# essa abordagem foif feita pois entre 1 e outro so mudar o 2 campos então montar 2 forms que vai ter apenas 2 camposd e diferença não e compensador  
class BaseInscritoForm(forms.ModelForm):
    motivos_acompanhamento = forms.MultipleChoiceField(
        choices=[
            ('ansiedade', 'Ansiedade'), ('assediomoral', 'Assédio Moral'), ('depressao', 'Depressão'),
            ('dfaprendizagem', 'Dificuldade de Aprendizagem'), ('humorinstavel', 'Humor Instável'),
            ('insonia', 'Insônia'), ('isolasocial', 'Isolamento Social'), ('luto', 'Luto'),
            ('tristeza', 'Tristeza'), ('apatia', 'Apatia'), ('chorofc', 'Choro Frequente'),
            ('exaustao', 'Exaustão'), ('fadiga', 'Fadiga'), ('faltanimo', 'Falta de Ânimo'),
            ('vldt', 'Vazio/Invalidez'), ('assediosexual', 'Assédio Sexual'), ('outro', 'Outro'),
        ],
        widget=forms.CheckboxSelectMultiple, label="Motivos da Busca do Tratamento", required=False
    )
    
    doencas_fisicas = forms.MultipleChoiceField(
        choices=[
            ('doencaresp', 'Doença Respiratória'), ('cancer', 'Câncer'), ('diabete', 'Diabetes'),
            ('disfusexual', 'Disfunção Sexual'), ('doencadgt', 'Doença Digestiva'), ('escleorosemlt', 'Esclerose Múltipla'),
            ('hcpt', 'Hipertensão'), ('luposatm', 'Lúpus'), ('obesidade', 'Obesidade'),
            ('pblmarenal', 'Problema Renal'), ('outro', 'Outro'),
        ],
        widget=forms.CheckboxSelectMultiple, label="Possui alguma doença física?", required=False
    )
    
    disponibilidade_semana = forms.MultipleChoiceField(
        choices=[('manha', 'Manhã'), ('tarde', 'Tarde'), ('noite', 'Noite'), ('sabado', 'Sábado')],
        widget=forms.CheckboxSelectMultiple, label="Qual sua disponibilidade?", required=True
    )
    
    pcd_neurodivergente = forms.MultipleChoiceField(
        choices=[
            ('tea', 'Autismo (TEA)'), ('tdah', 'TDAH'), ('dffs', 'Disfunção Fonoaudiológica'),
            ('dfv', 'Deficiência Visual'), ('dfa', 'Deficiência Auditiva'), ('ttap', 'Transtorno de Aprendizagem'),
            ('ahst', 'Altas Habilidades/Superdotação'), ('outro', 'Outro'),
        ],
        widget=forms.CheckboxSelectMultiple, label="Possui alguma deficiência ou neurodivergência?", required=False
    )

    tipo_terapias = forms.MultipleChoiceField(
        choices=[
            ('individualift', 'Individual Infantil'), ('individualadt', 'Individual Adolescente'),
            ('individualadto', 'Individual Adulto'), ('individualids', 'Individual Idoso'),
            ('familia', 'Atendimento à Família'), ('grupo', 'Atendimento em Grupo'), ('casal', 'Atendimento ao Casal'),
        ],
        widget=forms.CheckboxSelectMultiple, label="Qual tipo de terapia você busca?", required=True
    )
    
    medicamentos_usados = forms.MultipleChoiceField(
        choices=[
            ('ansiolitico', 'Ansiolítico'), ('antidepressivo', 'Antidepressivo'),
            ('antipsicotico', 'Antipsicótico'), ('estabhumeor', 'Estabilizador de Humor'),
            ('memoriatct', 'Memória/Concentração'), ('outro', 'Outro'),
        ],
        widget=forms.CheckboxSelectMultiple, label="Faz uso de algum medicamento psiquiátrico?", required=False
    )
    
    cidade = forms.CharField(max_length=40, label="Cidade")
    bairro = forms.CharField(max_length=50, required=False, label="Bairro")
    rua = forms.CharField(max_length=100, label="Rua/Avenida")
    uf = forms.CharField(max_length=2, initial='DF', label="UF")
    cep = forms.CharField(max_length=10, label="CEP")

#Salva o todos os campos do formulario base para poder facilita a instancia quanddo fori feito as classes filha
    def save(self, commit=True):
        inscrito = super().save(commit=False)
        
        if commit:
            inscrito.save()
            
            fk_data = {self._fk_name: inscrito} # Usado para criar a Fk que vai ser usada para guarda o nome do campo da chave estrageira

            motivos = Motivoacompanhamento(**fk_data) #criar a instância objeto, usando o fk_data para ja se referencia ao id do usuario que foi feito
            selected = self.cleaned_data.get('motivos_acompanhamento', []) # E uma funç do dicionario do django que ver todos os campos do formulario ja validados e se não tiver nada retorna um campo vazio
            for key, _ in self.fields['motivos_acompanhamento'].choices:# faz o loop de cada campo para a proxima linha ir verifacando qual vai ser true ou false no insert do banco
                setattr(motivos, key, key in selected)# Verificar qual True ou false para qual opção foi marcado 
            motivos.save() #Salva no banco de dados os novos dados , criado uma nova linha tabela do banco.

            doencas = Doencafisica(**fk_data)
            selected = self.cleaned_data.get('doencas_fisicas', [])
            for key, _ in self.fields['doencas_fisicas'].choices:
                setattr(doencas, key, key in selected)
            doencas.save()

            disponibilidade = Disponibilidade(**fk_data)
            selected = self.cleaned_data.get('disponibilidade_semana', [])
            for key, _ in self.fields['disponibilidade_semana'].choices:
                setattr(disponibilidade, key, key in selected)
            disponibilidade.save()

            pcd = Pcdsnd(**fk_data)
            selected = self.cleaned_data.get('pcd_neurodivergente', [])
            for key, _ in self.fields['pcd_neurodivergente'].choices:
                setattr(pcd, key, key in selected)
            pcd.save()

            terapia = Tipoterapia(**fk_data)
            selected = self.cleaned_data.get('tipo_terapias', [])
            for key, _ in self.fields['tipo_terapias'].choices:
                setattr(terapia, key, key in selected)
            terapia.save()

            medicamento = Medicamento(**fk_data)
            selected = self.cleaned_data.get('medicamentos_usados', [])
            for key, _ in self.fields['medicamentos_usados'].choices:
                setattr(medicamento, key, key in selected)
            medicamento.save()
            
            Endereco.objects.create(
                cidade=self.cleaned_data.get('cidade'),
                bairro=self.cleaned_data.get('bairro'),
                rua=self.cleaned_data.get('rua'),
                uf=self.cleaned_data.get('uf'),
                cep=self.cleaned_data.get('cep'),
                **fk_data
            )
            
        return inscrito #retorna o id e algumas informações do inscrito para confirmação de insert
        
    class Meta:
        abstract = True
        exclude = ['dthinscricao', 'status']

#
class InscritoComunidadeForm(BaseInscritoForm):
    _fk_name = 'idfichacomunidade'

    class Meta(BaseInscritoForm.Meta):
        #Faz a escolhar de qual models ele vai usar na inscricação nesso caso ele usar o models do formulario inscrito
        model = Inscritocomunidade
        fields = '__all__'
#Faz o novo form usando o baseinscritofomr como base e depois instacia o models especifico para adcionar as pequenas diferenças pequenas
class InscritoConvenioForm(BaseInscritoForm):
    _fk_name = 'idfichaconvenio'

    class Meta(BaseInscritoForm.Meta):
        model = Inscritoconvenio
        fields = '__all__'
        