import string
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

# --- 1. Formulário de Login (Que estava faltando) ---
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Digite sua Matrícula',
            'autofocus': True
        }),
        label="Matrícula"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sua Senha'
        }),
        label="Senha"
    )

# --- 2. Formulário de Cadastro (Com as correções de campos) ---
class CadastroUsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}),
        label='Senha',
        required=True,
        help_text="Requisito: 8-16 caracteres, maiúscula, minúscula, número e especial."
    )
    senha2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'}),
        label='Confirmação da senha',
        required=True
    )

    class Meta:
        model = Usuario
        fields = (
            'matricula', 'nome_completo', 'cpf', 'email', 'telefone', 
            'data_nascimento', 'cargo', 
            'crp', 'documento_crp', 
            'semestre', 'nivel_estagio', 'supervisor_vinculado'
        )
        
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select', 'id': 'id_cargo'}),
        }

    def clean_matricula(self):
        matricula = self.cleaned_data.get("matricula")
        usuario_id = getattr(self.instance, "id", None)
        if Usuario.objects.filter(matricula=matricula).exclude(id=usuario_id).exists():
            raise forms.ValidationError("Esta matrícula já está cadastrada.")
        return matricula

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
            return cpf
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        if len(cpf_limpo) != 11:
            raise forms.ValidationError("O CPF deve ter 11 dígitos.")
        
        usuario_id = getattr(self.instance, "id", None)
        if Usuario.objects.filter(cpf=cpf_limpo).exclude(id=usuario_id).exists():
            raise forms.ValidationError("CPF já cadastrado no sistema.")
            
        return cpf_limpo

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        senha2 = cleaned_data.get('senha2')
        cargo = cleaned_data.get('cargo')

        # Validação de Senha
        if senha:
            if len(senha) < 8 or len(senha) > 16:
                self.add_error('senha', 'A senha deve ter entre 8 e 16 caracteres.')
            if not any(char.isupper() for char in senha):
                self.add_error('senha', 'A senha precisa ter pelo menos uma letra maiúscula.')
            if not any(char.islower() for char in senha):
                self.add_error('senha', 'A senha precisa ter pelo menos uma letra minúscula.')
            if not any(char.isdigit() for char in senha):
                self.add_error('senha', 'A senha precisa ter pelo menos um número.')
            if not any(char in string.punctuation for char in senha):
                self.add_error('senha', 'A senha precisa ter um caractere especial (@, #, $, etc).')
            if senha != senha2:
                self.add_error('senha2', 'As senhas não conferem.')

        # Validação Condicional
        if cargo == 'ESTAG':
            if not cleaned_data.get('semestre'):
                self.add_error('semestre', 'O semestre é obrigatório para estagiários.')
            if not cleaned_data.get('nivel_estagio'):
                self.add_error('nivel_estagio', 'O nível do estágio é obrigatório.')
            cleaned_data['crp'] = None # Limpa CRP se for estagiário

        elif cargo in ['SUPER', 'RESP_TEC', 'COORD']:
            if not cleaned_data.get('crp'):
                self.add_error('crp', 'O número do CRP é obrigatório para este cargo.')
            
            # Upload obrigatório apenas na criação
            if not self.instance.pk and not cleaned_data.get('documento_crp'):
                 self.add_error('documento_crp', 'O upload do documento do CRP é obrigatório.')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        senha = self.cleaned_data.get('senha')
        if senha:
            usuario.set_password(senha)
        if commit:
            usuario.save()
        return usuario