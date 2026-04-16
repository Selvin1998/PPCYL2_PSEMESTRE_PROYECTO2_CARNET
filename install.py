#!/usr/bin/env python3
"""
Script de instalación automática para IPC2-AcadNet
Sistema de Gestión Educativa
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Ejecuta un comando y muestra el resultado"""
    try:
        print(f" ejecutando: {command}")
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  OK: {result.stdout.strip()}")
        else:
            print(f"  ERROR: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False
    return True

def check_python_version():
    """Verifica la versión de Python"""
    print("Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  ERROR: Se requiere Python 3.8 o superior (actual: {version.major}.{version.minor}.{version.micro})")
        return False

def check_pip():
    """Verifica si pip está instalado"""
    print("Verificando pip...")
    try:
        import pip
        print("  pip está instalado - OK")
        return True
    except ImportError:
        print("  ERROR: pip no está instalado")
        return False

def install_backend():
    """Instala el backend Flask"""
    print("\n=== Instalando Backend Flask ===")
    
    backend_dir = "backend_flask"
    if not os.path.exists(backend_dir):
        print(f"  ERROR: No se encuentra el directorio {backend_dir}")
        return False
    
    # Instalar dependencias del backend
    if not run_command("pip install -r requirements.txt", cwd=backend_dir):
        return False
    
    print("  Backend Flask instalado correctamente")
    return True

def install_frontend():
    """Instala el frontend Django"""
    print("\n=== Instalando Frontend Django ===")
    
    frontend_dir = "frontend_django"
    if not os.path.exists(frontend_dir):
        print(f"  ERROR: No se encuentra el directorio {frontend_dir}")
        return False
    
    # Instalar dependencias del frontend
    if not run_command("pip install -r requirements.txt", cwd=frontend_dir):
        return False
    
    # Ejecutar migraciones de Django
    if not run_command("python manage.py migrate", cwd=frontend_dir):
        return False
    
    print("  Frontend Django instalado correctamente")
    return True

def create_env_file():
    """Crea archivo .env.example si no existe"""
    print("\n=== Creando archivo de configuración ===")
    
    env_content = """# Configuración del Backend Flask
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=app.py

# Configuración del Frontend Django
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here

# URLs del sistema
BACKEND_URL=http://localhost:5000
FRONTEND_URL=http://localhost:8000

# Configuración de la base de datos (opcional)
DB_NAME=ipc2_acadnet
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
"""
    
    env_file = ".env.example"
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"  Archivo {env_file} creado")
    else:
        print(f"  Archivo {env_file} ya existe")
    
    return True

def create_startup_scripts():
    """Crea scripts de inicio para facilitar el uso"""
    print("\n=== Creando scripts de inicio ===")
    
    # Script para Windows
    windows_script = """@echo off
echo Iniciando IPC2-AcadNet
echo.

echo Iniciando Backend Flask...
start cmd /k "cd backend_flask && python app.py"

echo Esperando 3 segundos...
timeout /t 3 /nobreak >nul

echo Iniciando Frontend Django...
start cmd /k "cd frontend_django && python manage.py runserver"

echo.
echo Sistema iniciado correctamente!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
pause
"""
    
    with open("start_system.bat", 'w') as f:
        f.write(windows_script)
    print("  Script start_system.bat creado (Windows)")
    
    # Script para Linux/Mac
    linux_script = """#!/bin/bash
echo "Iniciando IPC2-AcadNet"
echo

echo "Iniciando Backend Flask..."
cd backend_flask && python app.py &
BACKEND_PID=$!

echo "Esperando 3 segundos..."
sleep 3

echo "Iniciando Frontend Django..."
cd frontend_django && python manage.py runserver &
FRONTEND_PID=$!

echo
echo "Sistema iniciado correctamente!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:8000"
echo
echo "Presiona Ctrl+C para detener el sistema"

# Esperar a que el usuario presione Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
"""
    
    with open("start_system.sh", 'w') as f:
        f.write(linux_script)
    
    # Hacer ejecutable el script de Linux/Mac
    if platform.system() != "Windows":
        run_command("chmod +x start_system.sh")
    
    print("  Script start_system.sh creado (Linux/Mac)")
    
    return True

def main():
    """Función principal de instalación"""
    print("=" * 60)
    print("  IPC2-AcadNet - Sistema de Gestión Educativa")
    print("  Script de Instalación Automática")
    print("=" * 60)
    
    # Verificar requisitos
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Instalar componentes
    if not install_backend():
        return False
    
    if not install_frontend():
        return False
    
    # Crear archivos de configuración
    create_env_file()
    create_startup_scripts()
    
    print("\n" + "=" * 60)
    print("  ¡INSTALACIÓN COMPLETADA!")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Inicia el sistema:")
    print("   - Windows: Ejecuta start_system.bat")
    print("   - Linux/Mac: Ejecuta ./start_system.sh")
    print("\n2. Accede a la aplicación:")
    print("   - Frontend: http://localhost:8000")
    print("   - Backend: http://localhost:5000")
    print("\n3. Usa las credenciales iniciales:")
    print("   - Administrador: admin123 / admin123")
    print("   - Tutor: tutor123 / tutor123")
    print("   - Estudiante: est123 / est123")
    print("\n4. Para más información, lee el archivo README.md")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        if main():
            sys.exit(0)
        else:
            print("\nERROR: La instalación falló. Revisa los mensajes de error.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nInstalación cancelada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR inesperado: {str(e)}")
        sys.exit(1)
