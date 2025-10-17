from django.urls import path
from . import views

app_name = 'formulario'

urlpatterns = [
    path('cadastro/comunidade/', views.comunidade, name='formulario_comuni'),
    path('cadastro/convenio/', views.convenio, name='formulario_conv')

]