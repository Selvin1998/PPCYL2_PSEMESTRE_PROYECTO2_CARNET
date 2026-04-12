from flask import Blueprint, request, jsonify
from data_store import db
import xml.etree.ElementTree as ET
import re

tutor_bp = Blueprint("tutor", __name__)

@tutor_bp.route("/cargar-horarios/<registro_personal>", methods=["POST"])
def cargar_horarios(registro_personal):
    try:
        xml_data = request.data.decode("utf-8").strip()
        root = ET.fromstring(xml_data)

        horarios_guardados = []
        horarios_invalidos = []

        # cursos asignados al tutor
        cursos_tutor = {
            a["codigo"]
            for a in db["asignaciones_tutores"]
            if a["registro_personal"] == registro_personal
        }

        for curso in root.findall("./curso"):
            codigo = curso.get("codigo")
            texto = (curso.text or "").strip()

            patron = r"HorarioI:\s*(\d{2}:\d{2})\s*HorarioF:\s*(\d{2}:\d{2})"
            coincidencia = re.search(patron, texto)

            if not codigo:
                horarios_invalidos.append({
                    "codigo": None,
                    "motivo": "Curso sin código"
                })
                continue

            if codigo not in cursos_tutor:
                horarios_invalidos.append({
                    "codigo": codigo,
                    "motivo": "Curso no asignado al tutor"
                })
                continue

            if not coincidencia:
                horarios_invalidos.append({
                    "codigo": codigo,
                    "motivo": "Formato de horario inválido"
                })
                continue

            hora_inicio = coincidencia.group(1)
            hora_fin = coincidencia.group(2)

            horario = {
                "registro_personal": registro_personal,
                "codigo": codigo,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin
            }

            db["horarios"].append(horario)
            horarios_guardados.append(horario)

        return jsonify({
            "status": "success",
            "message": "Horarios procesados",
            "resumen": {
                "guardados": len(horarios_guardados),
                "invalidos": len(horarios_invalidos)
            },
            "detalle": {
                "horarios_guardados": horarios_guardados,
                "horarios_invalidos": horarios_invalidos
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


@tutor_bp.route("/horarios/<registro_personal>", methods=["GET"])
def ver_horarios(registro_personal):
    horarios_tutor = [
        h for h in db["horarios"]
        if h["registro_personal"] == registro_personal
    ]

    return jsonify({
        "status": "success",
        "data": horarios_tutor
    })
