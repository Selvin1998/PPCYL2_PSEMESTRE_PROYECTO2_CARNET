from flask import Blueprint, request, jsonify
import xml.etree.ElementTree as ET

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/cargar-configuracion", methods=["POST"])
def cargar_configuracion():
    try:
        xml_data = request.data.decode("utf-8")

        root = ET.fromstring(xml_data)

        cursos = []
        for curso in root.findall(".//curso"):
            codigo = curso.find("codigo").text
            nombre = curso.find("nombre").text
            cursos.append({
                "codigo": codigo,
                "nombre": nombre
            })

        return jsonify({
            "status": "success",
            "message": "Configuración cargada",
            "cursos": cursos
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
