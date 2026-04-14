from django.urls import path
from . import views

urlpatterns = [
    # LOGIN
    path('', views.login_view, name='login'),

    # PANELES
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('tutor/', views.panel_tutor, name='panel_tutor'),
    path('estudiante/', views.panel_estudiante, name='panel_estudiante'),

    # FUNCIONALIDADES
    path('ver-notas/', views.ver_notas, name='ver_notas'),
    path('grafico/', views.grafico, name='grafico'),
    path('cargar-config/', views.cargar_config, name='cargar_config'),
    path('cargar-xml/', views.cargar_xml, name='cargar_xml'),
]