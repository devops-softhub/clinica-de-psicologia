from django.shortcuts import render

# Create your views here.

def comunidade(request):
    return render(request, 'formulario/comunidade_form.html')

def convenio(request):
    return render(request, 'formulario/convenio_form.html')