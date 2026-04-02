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

        # =========================
        # VALIDACIONES
        # =========================

        codigos_cursos = {c["codigo"] for c in cursos}
        registros_tutores = {t["registro_personal"] for t in tutores}
        carnets_estudiantes = {e["carnet"] for e in estudiantes}

        asignaciones_tutores_validas = []
        asignaciones_tutores_invalidas = []

        for a in asignaciones_tutores:
            if a["codigo"] in codigos_cursos and a["registro_personal"] in registros_tutores:
                asignaciones_tutores_validas.append(a)
            else:
                asignaciones_tutores_invalidas.append(a)

        asignaciones_estudiantes_validas = []
        asignaciones_estudiantes_invalidas = []

        for a in asignaciones_estudiantes:
            if a["codigo"] in codigos_cursos and a["carnet"] in carnets_estudiantes:
                asignaciones_estudiantes_validas.append(a)
            else:
                asignaciones_estudiantes_invalidas.append(a)

        # =========================
        # RESPUESTA FINAL
        # =========================

        return jsonify({
            "status": "success",
            "message": "Configuración cargada correctamente",
            "resumen": {
                "total_cursos": len(cursos),
                "total_tutores": len(tutores),
                "total_estudiantes": len(estudiantes),
                "total_asignaciones_tutores": len(asignaciones_tutores),
                "total_asignaciones_estudiantes": len(asignaciones_estudiantes),
                "tutores_validos": len(asignaciones_tutores_validas),
                "tutores_invalidos": len(asignaciones_tutores_invalidas),
                "estudiantes_validos": len(asignaciones_estudiantes_validas),
                "estudiantes_invalidos": len(asignaciones_estudiantes_invalidas)
            },
            "detalle": {
                "cursos": cursos,
                "tutores": tutores,
                "estudiantes": estudiantes,
                "asignaciones_tutores_validas": asignaciones_tutores_validas,
                "asignaciones_tutores_invalidas": asignaciones_tutores_invalidas,
                "asignaciones_estudiantes_validas": asignaciones_estudiantes_validas,
                "asignaciones_estudiantes_invalidas": asignaciones_estudiantes_invalidas
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
