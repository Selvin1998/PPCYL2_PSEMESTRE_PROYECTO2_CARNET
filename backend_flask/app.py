from flask import Flask, jsonify
from routes.auth import auth_bp

app = Flask(__name__)

# Ruta de prueba
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "success",
        "message": "API funcionando correctamente"
    })

# Registrar rutas (IMPORTANTE antes de correr)
app.register_blueprint(auth_bp, url_prefix="/api")

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
