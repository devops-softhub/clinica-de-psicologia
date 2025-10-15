from django.urls import path
from . import views

app_name = 'formulario'

urlpatterns = [
    path('', views.comunidade, name='formulario'),

]