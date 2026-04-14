from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Conecta con webapp
    path('', include('webapp.urls')),

    # Admin de Django (no tocar)
    path('admin/', admin.site.urls),
]