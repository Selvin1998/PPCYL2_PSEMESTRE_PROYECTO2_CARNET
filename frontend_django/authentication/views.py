from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm
from .services import login_backend, get_backend_status

def login_view(request):
    """
    Vista de login simplificada que solo pida contraseña y tipo de usuario
    """
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        
        # Mapeo de usuarios según el tipo
        user_credentials = {
            'admin': {'username': 'admin', 'password': 'admin123'},
            'tutor': {'username': '12345', 'password': 'tutor123'},
            'estudiante': {'username': '20230001', 'password': 'est123'}
        }
        
        if user_type in user_credentials:
            credentials = user_credentials[user_type]
            
            # Autenticar contra backend Flask
            result = login_backend(credentials['username'], password)
            
            if result.get('status') == 'success':
                # Guardar información en sesión
                request.session['user'] = result['user']
                request.session['role'] = result['role']
                request.session['logged_in'] = True
                
                messages.success(request, f"¡Bienvenido/a {result['user'].get('nombre', credentials['username'])}!")
                
                # Redirigir según rol
                if result['role'] == 'admin':
                    return redirect('/login/admin/')
                elif result['role'] == 'tutor':
                    return redirect('/login/tutor/')
                elif result['role'] == 'estudiante':
                    return redirect('/login/estudiante/')
                    
            else:
                messages.error(request, 'La contraseña es incorrecta')
        else:
            messages.error(request, 'Tipo de usuario no válido')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    """
    Cierra la sesión del usuario
    """
    request.session.flush()
    messages.success(request, "Has cerrado sesión correctamente")
    return redirect('/login/')

def dashboard_view(request):
    """
    Dashboard principal según el rol del usuario
    """
    if not request.session.get('logged_in'):
        return redirect('/login/')
    
    role = request.session.get('role')
    user = request.session.get('user')
    
    context = {
        'role': role,
        'user': user,
        'backend_status': get_backend_status()
    }
    
    # Redirigir a la vista específica según el rol
    if role == 'admin':
        return admin_view(request)
    elif role == 'tutor':
        return tutor_view(request)
    elif role == 'estudiante':
        return estudiante_view(request)
    else:
        return render(request, 'auth/dashboard.html', context)

def admin_view(request):
    """
    Vista para el administrador con funcionalidad de carga de archivos, revisión de usuarios e información
    """
    if not request.session.get('logged_in') or request.session.get('role') != 'admin':
        return redirect('/login/')
    
    user = request.session.get('user')
    usuarios_cargados = request.session.get('usuarios_cargados', [])
    xml_info = request.session.get('xml_info', {})
    seccion_activa = request.GET.get('seccion', 'usuarios')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'cargar_archivo':
            archivo = request.FILES.get('config_file')
            if archivo and archivo.name.endswith('.xml'):
                xml_content = archivo.read().decode('utf-8')
                try:
                    usuarios_cargados, xml_info = procesar_xml_admin(xml_content)
                    request.session['usuarios_cargados'] = usuarios_cargados
                    request.session['xml_info'] = xml_info
                    messages.success(request, f'Archivo XML cargado correctamente. Se encontraron {len(usuarios_cargados)} usuarios.')
                except Exception as e:
                    messages.error(request, f'Error al procesar el archivo XML: {str(e)}')
            else:
                messages.error(request, 'Por favor, selecciona un archivo XML válido')
        
        elif action == 'limpiar_usuarios':
            request.session['usuarios_cargados'] = []
            request.session['xml_info'] = {}
            messages.info(request, 'Lista de usuarios limpiada correctamente')
        
        elif action == 'generar_ejemplo':
            usuarios_cargados = generar_usuarios_ejemplo()
            xml_info = generar_info_ejemplo()
            request.session['usuarios_cargados'] = usuarios_cargados
            request.session['xml_info'] = xml_info
            messages.success(request, 'Datos de ejemplo generados correctamente')
        
        elif action == 'agregar_usuario':
            # Agregar nuevo usuario
            nuevo_usuario = {
                'id': len(usuarios_cargados) + 1,
                'usuario': request.POST.get('usuario', ''),
                'contrasena': request.POST.get('contrasena', ''),
                'tipo': request.POST.get('tipo', ''),
                'nombre': request.POST.get('nombre', ''),
                'registro': request.POST.get('registro', '') if request.POST.get('tipo') == 'Tutor' else '',
                'carnet': request.POST.get('carnet', '') if request.POST.get('tipo') == 'Estudiante' else ''
            }
            
            # Validar que el usuario no exista
            if not any(u['usuario'] == nuevo_usuario['usuario'] for u in usuarios_cargados):
                usuarios_cargados.append(nuevo_usuario)
                request.session['usuarios_cargados'] = usuarios_cargados
                messages.success(request, f'Usuario {nuevo_usuario["usuario"]} agregado correctamente')
            else:
                messages.error(request, 'El usuario ya existe')
        
        elif action == 'editar_usuario':
            # Editar usuario existente
            usuario_id = int(request.POST.get('usuario_id', 0))
            for i, usuario in enumerate(usuarios_cargados):
                if usuario['id'] == usuario_id:
                    usuarios_cargados[i] = {
                        'id': usuario_id,
                        'usuario': request.POST.get('usuario', usuario['usuario']),
                        'contrasena': request.POST.get('contrasena', usuario['contrasena']),
                        'tipo': request.POST.get('tipo', usuario['tipo']),
                        'nombre': request.POST.get('nombre', usuario['nombre']),
                        'registro': request.POST.get('registro', usuario.get('registro', '')),
                        'carnet': request.POST.get('carnet', usuario.get('carnet', ''))
                    }
                    request.session['usuarios_cargados'] = usuarios_cargados
                    messages.success(request, f'Usuario {usuarios_cargados[i]["usuario"]} actualizado correctamente')
                    break
        
        elif action == 'eliminar_usuario':
            # Eliminar usuario
            usuario_id = int(request.POST.get('usuario_id', 0))
            usuarios_cargados = [u for u in usuarios_cargados if u['id'] != usuario_id]
            request.session['usuarios_cargados'] = usuarios_cargados
            messages.success(request, 'Usuario eliminado correctamente')
    
    context = {
        'user': user,
        'usuarios_cargados': usuarios_cargados,
        'xml_info': xml_info,
        'seccion_activa': seccion_activa
    }
    
    return render(request, 'auth/admin_crud.html', context)

def procesar_xml_admin(xml_content):
    """
    Procesa el XML de configuración para el administrador
    """
    import xml.etree.ElementTree as ET
    
    try:
        root = ET.fromstring(xml_content)
        usuarios = []
        info = {
            'total_cursos': 0,
            'total_tutores': 0,
            'total_estudiantes': 0,
            'total_asignaciones': 0
        }
        
        # Procesar tutores
        for tutor in root.findall('.//tutor'):
            registro = tutor.find('registro_personal').text if tutor.find('registro_personal') is not None else ''
            nombre = tutor.find('nombre_del_tutor').text if tutor.find('nombre_del_tutor') is not None else ''
            contrasena = tutor.find('contrasenia').text if tutor.find('contrasenia') is not None else '******'
            
            if registro:
                usuarios.append({
                    'id': len(usuarios) + 1,
                    'usuario': f"Tutor_{registro}",
                    'contrasena': contrasena,
                    'tipo': 'Tutor',
                    'nombre': nombre,
                    'registro': registro
                })
                info['total_tutores'] += 1
        
        # Procesar estudiantes
        for estudiante in root.findall('.//estudiante'):
            carnet = estudiante.find('carnet').text if estudiante.find('carnet') is not None else ''
            nombre = estudiante.find('nombre_del_estudiante').text if estudiante.find('nombre_del_estudiante') is not None else ''
            contrasena = estudiante.find('contrasenia').text if estudiante.find('contrasenia') is not None else '******'
            
            if carnet:
                usuarios.append({
                    'id': len(usuarios) + 1,
                    'usuario': f"Estudiante_{carnet}",
                    'contrasena': contrasena,
                    'tipo': 'Estudiante',
                    'nombre': nombre,
                    'carnet': carnet
                })
                info['total_estudiantes'] += 1
        
        # Contar cursos y asignaciones
        info['total_cursos'] = len(root.findall('.//curso'))
        info['total_asignaciones'] = len(root.findall('.//asignaciones'))
        
        return usuarios, info
        
    except Exception as e:
        print(f"Error procesando XML de admin: {str(e)}")
        return [], {}

def generar_usuarios_ejemplo():
    """
    Genera datos de ejemplo para presentación
    """
    usuarios = [
        {'id': 1, 'usuario': 'admin_ppcyl', 'contrasena': 'AdminPPCYL2771', 'tipo': 'Administrador', 'nombre': 'Administrador Principal', 'registro': 'ADMIN001'},
        {'id': 2, 'usuario': 'tutor_12345', 'contrasena': 'tutor123', 'tipo': 'Tutor', 'nombre': 'Juan Pérez', 'registro': '12345'},
        {'id': 3, 'usuario': 'tutor_67890', 'contrasena': 'tutor456', 'tipo': 'Tutor', 'nombre': 'María García', 'registro': '67890'},
        {'id': 4, 'usuario': 'estudiante_20230001', 'contrasena': 'est123', 'tipo': 'Estudiante', 'nombre': 'Carlos López', 'carnet': '20230001'},
        {'id': 5, 'usuario': 'estudiante_20230002', 'contrasena': 'est456', 'tipo': 'Estudiante', 'nombre': 'Ana Martínez', 'carnet': '20230002'},
        {'id': 6, 'usuario': 'estudiante_20230003', 'contrasena': 'est789', 'tipo': 'Estudiante', 'nombre': 'Pedro Rodríguez', 'carnet': '20230003'},
        {'id': 7, 'usuario': 'tutor_11111', 'contrasena': 'tutor111', 'tipo': 'Tutor', 'nombre': 'Laura Sánchez', 'registro': '11111'},
        {'id': 8, 'usuario': 'estudiante_20230004', 'contrasena': 'est012', 'tipo': 'Estudiante', 'nombre': 'Diego Fernández', 'carnet': '20230004'},
        {'id': 9, 'usuario': 'estudiante_20230005', 'contrasena': 'est345', 'tipo': 'Estudiante', 'nombre': 'Sofía Torres', 'carnet': '20230005'},
        {'id': 10, 'usuario': 'tutor_22222', 'contrasena': 'tutor222', 'tipo': 'Tutor', 'nombre': 'Roberto Díaz', 'registro': '22222'}
    ]
    return usuarios

def generar_info_ejemplo():
    """
    Genera información de ejemplo para el sistema
    """
    return {
        'total_cursos': 4,
        'total_tutores': 4,
        'total_estudiantes': 5,
        'total_asignaciones': 9,
        'sistema_version': 'IPC2-AcadNet v1.0',
        'fecha_actual': '2025-04-15',
        'administrador_actual': 'AdminPPCYL2'
    }

def tutor_view(request):
    """
    Vista para el tutor con funcionalidad de horarios y notas
    """
    if not request.session.get('logged_in') or request.session.get('role') != 'tutor':
        return redirect('/login/')
    
    user = request.session.get('user')
    xml_content = ""
    horarios_procesados = {}
    archivo_cargado = False
    notas_generadas = request.session.get('notas_generadas', [])
    promedios = {}
    curso_seleccionado = request.GET.get('curso', '')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'cargar_horarios':
            archivo = request.FILES.get('horarios_file')
            if archivo and archivo.name.endswith('.xml'):
                xml_content = archivo.read().decode('utf-8')
                archivo_cargado = True
                
                # Procesar el XML para extraer horarios
                horarios_procesados = procesar_horarios_xml(xml_content, user)
                
                if horarios_procesados:
                    messages.success(request, f'Se cargaron {len(horarios_procesados)} horarios correctamente')
                else:
                    messages.warning(request, 'No se encontraron horarios para los cursos asignados')
            else:
                messages.error(request, 'Por favor, selecciona un archivo XML válido')
        
        elif action == 'generar_notas':
            notas_generadas = generar_notas_prueba(user)
            request.session['notas_generadas'] = notas_generadas
            messages.success(request, f'Se generaron {len(notas_generadas)} notas de prueba')
        
        elif action == 'generar_reporte':
            curso_seleccionado = request.POST.get('curso_seleccionado', '')
            if curso_seleccionado and notas_generadas:
                promedios = calcular_promedio_por_actividad(curso_seleccionado, notas_generadas)
                if promedios:
                    messages.success(request, f'Reporte generado para {curso_seleccionado}')
                else:
                    messages.warning(request, 'No hay notas para el curso seleccionado')
    
    # Si hay un curso seleccionado en GET, calcular promedios
    if curso_seleccionado and notas_generadas:
        promedios = calcular_promedio_por_actividad(curso_seleccionado, notas_generadas)
    
    context = {
        'user': user,
        'xml_content': xml_content,
        'horarios': horarios_procesados,
        'archivo_cargado': archivo_cargado,
        'notas_generadas': notas_generadas,
        'promedios': promedios,
        'curso_seleccionado': curso_seleccionado,
        'cursos_disponibles': ['XXX', 'YYY', 'ZZZ', 'WWW']
    }
    
    return render(request, 'auth/tutor_simple.html', context)

def procesar_horarios_xml(xml_content, user):
    """
    Procesa el XML de horarios y filtra por cursos asignados al tutor
    """
    import re
    from xml.etree import ElementTree as ET
    
    try:
        # Cursos asignados al tutor (ejemplo - deberías obtenerlos de la base de datos)
        cursos_asignados = ['XXX', 'YYY', 'ZZZ', 'WWW']  # Códigos de ejemplo
        
        # Parsear el XML
        root = ET.fromstring(xml_content)
        horarios = {}
        
        # Estructura para la tabla de horarios
        dias_semana = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']
        
        # Inicializar estructura de horarios
        for dia in dias_semana:
            horarios[dia] = {}
        
        # Buscar todos los elementos que contienen horarios
        for elemento in root.iter():
            if elemento.text:
                texto = elemento.text
                
                # Extraer código del curso y horarios usando expresiones regulares
                # Buscar patrón: CódigoCurso - NombreCurso y HorarioI: HH:mm HorarioF: HH:mm
                curso_match = re.search(r'([A-Z]{3,4})\s*-\s*([^:]+)', texto)
                horario_match = re.search(r'HorarioI:\s*(\d{2}:\d{2})\s*HorarioF:\s*(\d{2}:\d{2})', texto)
                
                if curso_match and horario_match:
                    codigo_curso = curso_match.group(1)
                    nombre_curso = curso_match.group(2).strip()
                    hora_inicio = horario_match.group(1)
                    hora_fin = horario_match.group(2)
                    
                    # Filtrar solo cursos asignados al tutor
                    if codigo_curso in cursos_asignados:
                        # Determinar el día (aquí necesitarías lógica adicional para identificar el día)
                        # Por ahora, asumiremos que todos los horarios son para todos los días
                        for dia in dias_semana:
                            curso_key = f"{codigo_curso} - {nombre_curso}"
                            if curso_key not in horarios[dia]:
                                horarios[dia][curso_key] = []
                            horarios[dia][curso_key].append(f"{hora_inicio} - {hora_fin}")
        
        return horarios
        
    except Exception as e:
        print(f"Error procesando XML: {str(e)}")
        return {}

def generar_notas_prueba(user):
    """
    Genera notas de prueba para los cursos asignados al tutor
    """
    import random
    
    # Datos de ejemplo para cursos y actividades
    cursos_ejemplo = {
        'XXX': {
            'nombre': 'Matemáticas Discretas',
            'actividades': ['Tarea1', 'Tarea2', 'Examen Parcial', 'Proyecto Final'],
            'estudiantes': ['20230001', '20230002', '20230003', '20230004', '20230005']
        },
        'YYY': {
            'nombre': 'Programación Avanzada',
            'actividades': ['Laboratorio 1', 'Laboratorio 2', 'Examen Final'],
            'estudiantes': ['20230006', '20230007', '20230008', '20230009']
        },
        'ZZZ': {
            'nombre': 'Bases de Datos',
            'actividades': ['Diseño ER', 'Consultas SQL', 'Proyecto BD'],
            'estudiantes': ['20230010', '20230011', '20230012', '20230013', '20230014']
        },
        'WWW': {
            'nombre': 'Redes de Computadoras',
            'actividades': ['Configuración Router', 'Subnetting', 'Seguridad Redes'],
            'estudiantes': ['20230015', '20230016', '20230017']
        }
    }
    
    notas_generadas = []
    
    for curso_id, data in cursos_ejemplo.items():
        for actividad in data['actividades']:
            for estudiante in data['estudiantes']:
                # Generar nota aleatoria entre 0 y 100
                nota_valor = random.randint(0, 100)
                
                nota = {
                    'tutor_id': user.get('registro_personal', '12345'),
                    'curso_id': curso_id,
                    'curso_nombre': data['nombre'],
                    'actividad_nombre': actividad,
                    'estudiante_carnet': estudiante,
                    'valor': nota_valor
                }
                notas_generadas.append(nota)
    
    return notas_generadas

def calcular_promedio_por_actividad(curso_id, notas):
    """
    Calcula el promedio de notas por actividad para un curso específico
    """
    # Filtrar notas por curso
    notas_curso = [n for n in notas if n['curso_id'] == curso_id]
    
    if not notas_curso:
        return {}
    
    # Agrupar por actividad y calcular promedio
    actividades = {}
    for nota in notas_curso:
        actividad = nota['actividad_nombre']
        if actividad not in actividades:
            actividades[actividad] = []
        actividades[actividad].append(nota['valor'])
    
    # Calcular promedios
    promedios = {}
    for actividad, valores in actividades.items():
        promedio = sum(valores) / len(valores)
        promedios[actividad] = {
            'promedio': round(promedio, 2),
            'cantidad': len(valores),
            'maximo': max(valores),
            'minimo': min(valores)
        }
    
    return promedios

def estudiante_view(request):
    """
    Vista para el estudiante con funcionalidad de notas y procesamiento
    """
    if not request.session.get('logged_in') or request.session.get('role') != 'estudiante':
        return redirect('/login/')
    
    user = request.session.get('user')
    notas_estudiante = []
    cursos_asignados = []
    curso_seleccionado = request.GET.get('curso', '')
    xml_config = request.session.get('xml_config', {})
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'cargar_config':
            archivo = request.FILES.get('config_file')
            if archivo and archivo.name.endswith('.xml'):
                xml_content = archivo.read().decode('utf-8')
                xml_config = procesar_xml_configuracion(xml_content)
                request.session['xml_config'] = xml_config
                
                # Obtener cursos asignados al estudiante
                cursos_asignados = obtener_cursos_estudiante(user['carnet'], xml_config)
                
                messages.success(request, f'Configuración cargada correctamente')
            else:
                messages.error(request, 'Por favor, selecciona un archivo XML válido')
        
        elif action == 'consultar_notas':
            curso_seleccionado = request.POST.get('curso_seleccionado', '')
            if curso_seleccionado and xml_config:
                notas_estudiante = obtener_notas_estudiante(user['carnet'], curso_seleccionado, xml_config)
                if notas_estudiante:
                    messages.success(request, f'Se encontraron {len(notas_estudiante)} notas')
                else:
                    messages.warning(request, 'No se encontraron notas para este curso')
    
    # Si hay configuración, obtener cursos asignados
    if xml_config and not cursos_asignados:
        cursos_asignados = obtener_cursos_estudiante(user['carnet'], xml_config)
    
    context = {
        'user': user,
        'notas_estudiante': notas_estudiante,
        'cursos_asignados': cursos_asignados,
        'curso_seleccionado': curso_seleccionado,
        'xml_config': xml_config
    }
    
    return render(request, 'auth/estudiante.html', context)

def procesar_xml_configuracion(xml_content):
    """
    Procesa el XML de configuración del sistema
    """
    import xml.etree.ElementTree as ET
    
    try:
        root = ET.fromstring(xml_content)
        config = {
            'cursos': {},
            'tutores': {},
            'estudiantes': {},
            'asignaciones_tutores': {},
            'asignaciones_estudiantes': {}
        }
        
        # Procesar cursos
        for curso in root.findall('.//curso'):
            codigo = curso.find('codigo').text if curso.find('codigo') is not None else ''
            nombre = curso.find('Nombre_del_curso').text if curso.find('Nombre_del_curso') is not None else ''
            if codigo:
                config['cursos'][codigo] = nombre
        
        # Procesar tutores
        for tutor in root.findall('.//tutor'):
            registro = tutor.find('registro_personal').text if tutor.find('registro_personal') is not None else ''
            nombre = tutor.find('nombre_del_tutor').text if tutor.find('nombre_del_tutor') is not None else ''
            if registro:
                config['tutores'][registro] = nombre
        
        # Procesar estudiantes
        for estudiante in root.findall('.//estudiante'):
            carnet = estudiante.find('carnet').text if estudiante.find('carnet') is not None else ''
            nombre = estudiante.find('nombre_del_estudiante').text if estudiante.find('nombre_del_estudiante') is not None else ''
            if carnet:
                config['estudiantes'][carnet] = nombre
        
        # Procesar asignaciones de tutores
        for asignacion in root.findall('.//c_tutores//tutor_curso'):
            codigo = asignacion.find('codigo').text if asignacion.find('codigo') is not None else ''
            registro = asignacion.find('registro_personal').text if asignacion.find('registro_personal') is not None else ''
            if codigo and registro:
                if codigo not in config['asignaciones_tutores']:
                    config['asignaciones_tutores'][codigo] = []
                config['asignaciones_tutores'][codigo].append(registro)
        
        # Procesar asignaciones de estudiantes
        for asignacion in root.findall('.//c_estudiante//estudiante_curso'):
            codigo = asignacion.find('codigo').text if asignacion.find('codigo') is not None else ''
            carnet = asignacion.find('carnet').text if asignacion.find('carnet') is not None else ''
            if codigo and carnet:
                if codigo not in config['asignaciones_estudiantes']:
                    config['asignaciones_estudiantes'][codigo] = []
                config['asignaciones_estudiantes'][codigo].append(carnet)
        
        return config
        
    except Exception as e:
        print(f"Error procesando XML de configuración: {str(e)}")
        return {}

def obtener_cursos_estudiante(carnet, xml_config):
    """
    Obtiene los cursos asignados a un estudiante
    """
    cursos = []
    for codigo, estudiantes in xml_config.get('asignaciones_estudiantes', {}).items():
        if carnet in estudiantes:
            cursos.append({
                'codigo': codigo,
                'nombre': xml_config.get('cursos', {}).get(codigo, f'Curso {codigo}')
            })
    return cursos

def obtener_notas_estudiante(carnet, curso_codigo, xml_config):
    """
    Obtiene las notas de un estudiante para un curso específico
    """
    # Simular notas basadas en las notas generadas por el tutor
    # En un sistema real, esto vendría de la base de datos
    import random
    
    actividades_por_curso = {
        'XXX': ['Tarea1', 'Tarea2', 'Examen Parcial', 'Proyecto Final'],
        'YYY': ['Laboratorio 1', 'Laboratorio 2', 'Examen Final'],
        'ZZZ': ['Diseño ER', 'Consultas SQL', 'Proyecto BD'],
        'WWW': ['Configuración Router', 'Subnetting', 'Seguridad Redes']
    }
    
    notas = []
    if curso_codigo in actividades_por_curso:
        for actividad in actividades_por_curso[curso_codigo]:
            # Generar nota aleatoria entre 0 y 100
            nota_valor = random.randint(0, 100)
            notas.append({
                'actividad': actividad,
                'nota': nota_valor,
                'estado': 'Aprobado' if nota_valor >= 60 else 'Reprobado'
            })
    
    return notas

def procesar_xml(xml_content):
    """
    Función para procesar el contenido XML
    """
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_content)
        
        # Aquí puedes agregar la lógica específica de procesamiento
        # Por ahora, solo devolvemos el XML formateado
        return ET.tostring(root, encoding='unicode', method='xml')
    except Exception as e:
        return f"Error procesando XML: {str(e)}"

def api_status_view(request):
    """
    API endpoint para verificar estado del backend
    """
    status = get_backend_status()
    return JsonResponse(status)
