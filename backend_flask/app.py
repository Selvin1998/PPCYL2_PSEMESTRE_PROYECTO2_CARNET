from flask import Flask, jsonify
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.tutor import tutor_bp
from routes.notas import notas_bp

app = Flask(__name__)

# Configuración CORS para comunicación con frontend Django
from flask_cors import CORS
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "success",
        "message": "API funcionando correctamente"
    })

# Registrar rutas
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")
app.register_blueprint(tutor_bp, url_prefix="/api")
app.register_blueprint(notas_bp, url_prefix="/api")

#CREAR UNA RUTA DE PRUEBA
@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "status": "success",
        "message": "¡Hola! Esta es una ruta de prueba",
        "data": {
            "saludo": "Bienvenido a la API",
            "timestamp": "2026-04-15"
        }
    })

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)


