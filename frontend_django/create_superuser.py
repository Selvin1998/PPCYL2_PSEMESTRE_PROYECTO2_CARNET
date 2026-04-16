import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_frontend.settings')
django.setup()

from django.contrib.auth.models import User

# Crear superusuario
try:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuario creado exitosamente:')
    print('Usuario: admin')
    print('Contraseña: admin123')
except Exception as e:
    print(f'Error: {e}')
    print('El usuario admin ya existe')
