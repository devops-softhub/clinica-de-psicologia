from django.urls import path
from . import views # Garante que está a importar o views.py do Passo 2

app_name = 'formulario'

urlpatterns = [
    path('cadastro/comunidade/', views.formulario_comunidade_view, name='formulario_comunidade'),
]

