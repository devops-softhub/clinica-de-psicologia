from django import forms

class InscricaoForm(forms.Form):
# dados do paciente 
    nome_completo = forms.CharField(
        label='Nome Completo',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Nome Completo', 'class': 'apenas-letras'})
    )
    CPF = forms.CharFieldField(
        label='CPF',
        max_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'CPF', 'class': 'cpf', 'maxlength':'11'})
    )
    data_nascimento = forms.DateField(
        label='Data_nascimento',
        widget=forms.DateInput(attrs={ 'type' : 'date' })
    )
    rua= forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'Rua'}))
    bairro= forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Bairro'}))
    cidade=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Cidade'}))
    cep=forms.CharField(max_length=9, widget=forms.TextInput(attrs={'placeholder':'CEP'}))