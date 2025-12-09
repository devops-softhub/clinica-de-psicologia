from django.urls import path
from . import views

app_name = 'estagiario'

urlpatterns = [
    path('dashboard/', views.dashboard_estagiario, name='home'),
]
