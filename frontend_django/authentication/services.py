import requests
from django.conf import settings
from django.contrib import messages

def login_backend(username, password):
    """
    Autentica usuario contra el backend Flask
    """
    try:
        url = f"{settings.BACKEND_URL}/login"
        data = {
            'username': username,
            'password': password
        }
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
            
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': f'Error de conexión con el backend: {str(e)}'
        }

def get_backend_status():
    """
    Verifica el estado del backend Flask
    """
    try:
        url = f"{settings.BACKEND_URL.replace('/api', '')}/health"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'error', 'message': 'Backend no disponible'}
            
    except requests.exceptions.RequestException:
        return {'status': 'error', 'message': 'Backend no disponible'}
