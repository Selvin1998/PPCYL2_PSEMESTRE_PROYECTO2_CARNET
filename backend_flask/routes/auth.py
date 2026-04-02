from flask import Blueprint, request, jsonify
from data_store import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Debe enviar un JSON válido"
            }), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "status": "error",
                "message": "Faltan username o password"
            }), 400

        # Login admin
        if (
            username == db["admin"]["username"] and
            password == db["admin"]["password"]
        ):
            return jsonify({
                "status": "success",
                "message": "Login correcto",
                "role": "admin",
                "user": {
                    "username": username
                }
            })

        # Login tutores
        for tutor in db["tutores"]:
            if (
                username == tutor["registro_personal"] and
                password == tutor["contrasenia"]
            ):
                return jsonify({
                    "status": "success",
                    "message": "Login correcto",
                    "role": "tutor",
                    "user": {
                        "registro_personal": tutor["registro_personal"],
                        "nombre": tutor["nombre"]
                    }
                })

        # Login estudiantes
        for estudiante in db["estudiantes"]:
            if (
                username == estudiante["carnet"] and
                password == estudiante["contrasenia"]
            ):
                return jsonify({
                    "status": "success",
                    "message": "Login correcto",
                    "role": "estudiante",
                    "user": {
                        "carnet": estudiante["carnet"],
                        "nombre": estudiante["nombre"]
                    }
                })

        return jsonify({
            "status": "error",
            "message": "Credenciales incorrectas"
        }), 401

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
