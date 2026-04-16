from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/', views.admin_view, name='admin'),
    path('tutor/', views.tutor_view, name='tutor'),
    path('estudiante/', views.estudiante_view, name='estudiante'),
    path('api/status/', views.api_status_view, name='api_status'),
]
