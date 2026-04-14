from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from matriz import MatrizDispersa
from usuarios import SistemaUsuarios

app = Flask(__name__)

# Sistemas globales
matriz = MatrizDispersa()
sistema = SistemaUsuarios()


# -------------------------
# INICIO
# -------------------------
@app.route('/')
def inicio():
    return "API funcionando correctamente"


# -------------------------
# LOGIN
# -------------------------
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)  # 🔥 FIX

        usuario = data.get('usuario')
        password = data.get('password')

        resultado = sistema.login(usuario, password)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# CARGAR CONFIGURACIÓN
# -------------------------
@app.route('/cargarConfiguracion', methods=['POST'])
def cargar_configuracion():
    try:
        xml_data = request.data.decode('utf-8')
        root = ET.fromstring(xml_data)

        tutores = root.find('tutores')
        if tutores:
            for t in tutores.findall('tutor'):
                sistema.agregar_usuario(
                    t.get('registro_personal'),
                    t.get('contrasenia'),
                    "tutor"
                )

        estudiantes = root.find('estudiantes')
        if estudiantes:
            for e in estudiantes.findall('estudiante'):
                sistema.agregar_usuario(
                    e.get('carnet'),
                    e.get('contrasenia'),
                    "estudiante"
                )

        # ADMIN FIJO
        sistema.agregar_usuario("AdminPPCYL2", "AdminPPCYL2771", "admin")

        return jsonify({"mensaje": "Configuración cargada correctamente"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# CARGAR NOTAS
# -------------------------
@app.route('/cargarNotas', methods=['POST'])
def cargar_notas():
    try:
        xml_data = request.data.decode('utf-8')
        root = ET.fromstring(xml_data)

        notas = root.find('notas')

        if notas:
            for actividad in notas.findall('actividad'):
                matriz.insertar(
                    actividad.get('nombre'),
                    actividad.get('carnet'),
                    int(actividad.text)
                )

            return jsonify({"mensaje": "Notas cargadas correctamente"})

        return jsonify({"error": "No se encontró <notas>"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# VER NOTAS
# -------------------------
@app.route('/verNotas', methods=['GET'])
def ver_notas():
    try:
        lista = []

        for nodo in matriz.nodos:
            lista.append({
                "actividad": nodo.fila,
                "carnet": nodo.columna,
                "nota": nodo.valor
            })

        return jsonify({"notas": lista})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# GRAFICO (🔥 MOVIDO ARRIBA)
# -------------------------
@app.route('/grafico', methods=['GET'])
def grafico():
    try:
        datos = {}

        for nodo in matriz.nodos:
            actividad = nodo.fila

            if actividad not in datos:
                datos[actividad] = []

            datos[actividad].append(nodo.valor)

        promedios = []

        for act, notas in datos.items():
            promedio = sum(notas) / len(notas)
            promedios.append({
                "actividad": act,
                "promedio": promedio
            })

        return jsonify(promedios)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# REPORTE
# -------------------------
@app.route('/reporte', methods=['GET'])
def reporte():
    try:
        matriz.generar_reporte()
        return jsonify({"mensaje": "Reporte generado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# RUN (SIEMPRE AL FINAL)
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)