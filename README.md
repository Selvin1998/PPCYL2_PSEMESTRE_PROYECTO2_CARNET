# IPC2-AcadNet - Sistema de Gestión Educativa

Sistema completo de gestión - tres perfiles de usuario: Administrador, Tutor y Estudiante. Implementado con backend Flask y frontend Django.

## Características Principales

### Perfil Administrador
- **Gestión CRUD de usuarios**: Agregar, editar y eliminar usuarios
- **Carga de archivos XML**: Configuración del sistema
- **Estadísticas del sistema**: Información detallada de usuarios y cursos
- **Generación de datos de ejemplo**: Para presentaciones y pruebas

### Perfil Tutor
- **Gestión de horarios**: Carga y procesamiento de archivos XML
- **Generación de notas**: Creación automática de notas de prueba
- **Reportes académicos**: Gráficos y estadísticas
- **Exportación de datos**: Generación de archivos PDF

### Perfil Estudiante
- **Consulta de notas**: Visualización por curso y actividad
- **Configuración personal**: Carga de archivos XML de configuración
- **Estadísticas académicas**: Promedios y resúmenes
- **Generación de reportes**: Exportación de datos personales

## Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

## Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Selvin1998/PPCYL2_PSEMESTRE_PROYECTO2_CARNET.git
cd PPCYL2_PSEMESTRE_PROYECTO2_CARNET
```

### 2. Instalación Automática (Recomendado)
```bash
# Windows
python install.py

# Linux/Mac
python3 install.py
```

### 3. Instalación Manual

#### Backend Flask
```bash
cd backend_flask
pip install -r requirements.txt
python app.py
```

#### Frontend Django
```bash
cd frontend_django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Configuración Inicial

### 1. Backend Flask
El backend se ejecuta automáticamente en `http://localhost:5000`

### 2. Frontend Django
Accede a la aplicación en `http://localhost:8000`

### 3. Credenciales de Acceso Iniciales

| Perfil | Usuario | Contraseña |
|--------|---------|------------|
| Administrador | admin123 | admin123 |
| Tutor | tutor123 | tutor123 |
| Estudiante | est123 | est123 |

## Guía de Uso

### Para Administradores

1. **Iniciar sesión**: Usa las credenciales de administrador
2. **Cargar configuración**: Sube archivos XML con la configuración del sistema
3. **Gestionar usuarios**: Agrega, edita o elimina usuarios del sistema
4. **Generar datos**: Usa datos de ejemplo para pruebas y presentaciones

### Para Tutores

1. **Cargar horarios**: Sube archivos XML con tus horarios de clase
2. **Generar notas**: Crea notas de prueba para tus cursos asignados
3. **Ver reportes**: Consulta estadísticas y genera gráficos
4. **Exportar datos**: Descarga reportes en formato PDF

### Para Estudiantes

1. **Configurar perfil**: Sube archivos XML con tu configuración personal
2. **Consultar notas**: Revisa tus notas por curso y actividad
3. **Ver estadísticas**: Consulta tus promedios y rendimiento académico
4. **Generar reportes**: Exporta tus datos académicos

## Estructura del Proyecto

```
PPCYL2_PSEMESTRE_PROYECTO2_CARNET/
|
 backend_flask/                 # Backend Flask
|   app.py                     # API principal
|   data_store.py              # Gestión de datos
|   requirements.txt           # Dependencias del backend
|
 frontend_django/              # Frontend Django
|   manage.py                  # Script de gestión Django
|   requirements.txt           # Dependencias del frontend
|   proyecto_frontend/         # Configuración del proyecto
|   authentication/            # Módulo de autenticación
|   admin/                     # Módulo administrador
|   tutor/                     # Módulo tutor
|   notas/                     # Módulo de notas
|   templates/                 # Templates HTML
|
 install.py                    # Script de instalación automática
 README.md                     # Documentación del proyecto
```

## Archivos de Configuración

### Formato XML para Administradores
```xml
<configuracion>
    <tutores>
        <tutor>
            <registro_personal>12345</registro_personal>
            <nombre_del_tutor>Juan Pérez</nombre_del_tutor>
            <contrasenia>password123</contrasenia>
        </tutor>
    </tutores>
    <estudiantes>
        <estudiante>
            <carnet>20230001</carnet>
            <nombre_del_estudiante>Carlos López</nombre_del_estudiante>
            <contrasenia>est123</contrasenia>
        </estudiante>
    </estudiantes>
    <cursos>
        <curso>
            <codigo>XXX</codigo>
            <nombre>Matemáticas</nombre>
        </curso>
    </cursos>
</configuracion>
```

### Formato XML para Tutores
```xml
<horarios>
    <horario>
        <curso>XXX</curso>
        <dia>Lunes</dia>
        <horarioI>08:00</horarioI>
        <horarioF>10:00</horarioF>
        <aula>A101</aula>
    </horario>
</horarios>
```

## Solución de Problemas

### Problemas Comunes

1. **Error de puerto en uso**
   - Cambia el puerto en `frontend_django/manage.py runserver 8001`

2. **Error de dependencias**
   - Ejecuta `pip install -r requirements.txt` en cada carpeta

3. **Error de migraciones**
   - Ejecuta `python manage.py migrate --run-syncdb`

4. **Error de CORS**
   - Asegúrate que el backend Flask esté corriendo en el puerto 5000

### Comandos Útiles

```bash
# Verificar instalación de Django
python -m django --version

# Crear superusuario (opcional)
python manage.py createsuperuser

# Verificar estado del servidor
python manage.py check

# Limpiar caché de Django
python manage.py clearsessions
```

## Personalización

### Cambiar Credenciales
Edita los archivos de configuración en `frontend_django/authentication/services.py`

### Modificar Estilos
Los archivos CSS están en `frontend_django/templates/base.html`

### Agregar Nuevas Funcionalidades
Crea nuevas vistas en los módulos correspondientes:
- `frontend_django/authentication/views.py`
- `frontend_django/admin/views.py`
- `frontend_django/tutor/views.py`

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de Solución de Problemas
2. Abre un issue en GitHub
3. Contacta al desarrollador

