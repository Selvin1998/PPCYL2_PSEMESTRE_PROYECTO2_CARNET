from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

# usuario admin fijo
ADMIN_USER = "AdminPPCYL2"
ADMIN_PASS = "AdminPPCYL2771"

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username == ADMIN_USER and password == ADMIN_PASS:
        return jsonify({
            "status": "success",
            "message": "Login correcto",
            "role": "admin"
        })
    
    return jsonify({
        "status": "error",
        "message": "Credenciales incorrectas"
    }), 401
