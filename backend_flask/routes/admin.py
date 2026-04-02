from flask import Blueprint, request, jsonify
import xml.etree.ElementTree as ET

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/cargar-configuracion", methods=["POST"])
def cargar_configuracion():
    try:
        xml_data = request.data.decode("utf-8").strip()
        root = ET.fromstring(xml_data)

        cursos = []
        tutores = []
        estudiantes = []
        asignaciones_tutores = []
        asignaciones_estudiantes = []

        # Cursos
        for curso in root.findall("./cursos/curso"):
            codigo = curso.get("codigo")
            nombre = (curso.text or "").strip()

            if codigo and nombre:
                cursos.append({
                    "codigo": codigo,
                    "nombre": nombre
                })

        # Tutores
        for tutor in root.findall("./tutores/tutor"):
            registro_personal = tutor.get("registro_personal")
            contrasenia = tutor.get("contrasenia")
            nombre = (tutor.text or "").strip()

            if registro_personal and contrasenia and nombre:
                tutores.append({
                    "registro_personal": registro_personal,
                    "contrasenia": contrasenia,
                    "nombre": nombre
                })

        # Estudiantes
        for estudiante in root.findall("./estudiantes/estudiante"):
            carnet = estudiante.get("carnet")
            contrasenia = estudiante.get("contrasenia")
            nombre = (estudiante.text or "").strip()

            if carnet and contrasenia and nombre:
                estudiantes.append({
                    "carnet": carnet,
                    "contrasenia": contrasenia,
                    "nombre": nombre
                })

        # Asignaciones tutor-curso
        for asignacion in root.findall("./asignaciones/c_tutores/tutor_curso"):
            codigo = asignacion.get("codigo")
            registro_personal = (asignacion.text or "").strip()

            if codigo and registro_personal:
                asignaciones_tutores.append({
                    "codigo": codigo,
                    "registro_personal": registro_personal
                })

        # Asignaciones estudiante-curso
        for asignacion in root.findall("./asignaciones/c_estudiante/estudiante_curso"):
            codigo = asignacion.get("codigo")
            carnet = (asignacion.text or "").strip()

            if codigo and carnet:
                asignaciones_estudiantes.append({
                    "codigo": codigo,
                    "carnet": carnet
                })

        return jsonify({
            "status": "success",
            "message": "Configuración cargada correctamente",
            "data": {
                "cursos": cursos,
                "tutores": tutores,
                "estudiantes": estudiantes,
                "asignaciones_tutores": asignaciones_tutores,
                "asignaciones_estudiantes": asignaciones_estudiantes
            }
        })

    except ET.ParseError:
        return jsonify({
            "status": "error",
            "message": "XML inválido"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
