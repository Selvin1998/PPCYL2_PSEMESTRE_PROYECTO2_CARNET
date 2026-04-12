from flask import Blueprint, request, jsonify
import xml.etree.ElementTree as ET
from data_store import db
from matriz_dispersa import MatrizDispersa

notas_bp = Blueprint("notas", __name__)

@notas_bp.route("/tutor/cargar-notas/<registro_personal>", methods=["POST"])
def cargar_notas(registro_personal):
    try:
        xml_data = request.data.decode("utf-8").strip()
        root = ET.fromstring(xml_data)

        curso_tag = root.find("./curso")
        if curso_tag is None:
            return jsonify({
                "status": "error",
                "message": "No se encontró la etiqueta curso"
            }), 400

        codigo_curso = curso_tag.get("codigo")
        nombre_curso = (curso_tag.text or "").strip()

        if not codigo_curso:
            return jsonify({
                "status": "error",
                "message": "El curso no tiene código"
            }), 400

        curso_pertenece = any(
            a["codigo"] == codigo_curso and a["registro_personal"] == registro_personal
            for a in db["asignaciones_tutores"]
        )

        if not curso_pertenece:
            return jsonify({
                "status": "error",
                "message": "El curso no está asignado a este tutor"
            }), 400

        if codigo_curso not in db["notas"]:
            db["notas"][codigo_curso] = MatrizDispersa()

        matriz = db["notas"][codigo_curso]

        notas_guardadas = []
        notas_invalidas = []

        for actividad in root.findall("./notas/actividad"):
            nombre_actividad = actividad.get("nombre")
            carnet = actividad.get("carnet")
            texto_nota = (actividad.text or "").strip()

            if not nombre_actividad or not carnet or not texto_nota:
                notas_invalidas.append({
                    "actividad": nombre_actividad,
                    "carnet": carnet,
                    "motivo": "Datos incompletos"
                })
                continue

            try:
                nota = float(texto_nota)
            except ValueError:
                notas_invalidas.append({
                    "actividad": nombre_actividad,
                    "carnet": carnet,
                    "motivo": "Nota no numérica"
                })
                continue

            if nota < 0 or nota > 100:
                notas_invalidas.append({
                    "actividad": nombre_actividad,
                    "carnet": carnet,
                    "motivo": "Nota fuera de rango"
                })
                continue

            estudiante_valido = any(
                a["codigo"] == codigo_curso and a["carnet"] == carnet
                for a in db["asignaciones_estudiantes"]
            )

            if not estudiante_valido:
                notas_invalidas.append({
                    "actividad": nombre_actividad,
                    "carnet": carnet,
                    "motivo": "Estudiante no asignado al curso"
                })
                continue

            matriz.insertar(nombre_actividad, carnet, nota)

            notas_guardadas.append({
                "actividad": nombre_actividad,
                "carnet": carnet,
                "nota": nota
            })

        return jsonify({
            "status": "success",
            "message": "Notas procesadas correctamente",
            "curso": {
                "codigo": codigo_curso,
                "nombre": nombre_curso
            },
            "resumen": {
                "guardadas": len(notas_guardadas),
                "invalidas": len(notas_invalidas)
            },
            "detalle": {
                "notas_guardadas": notas_guardadas,
                "notas_invalidas": notas_invalidas
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


@notas_bp.route("/estudiante/notas/<carnet>/<codigo_curso>", methods=["GET"])
def ver_notas_estudiante(carnet, codigo_curso):
    if codigo_curso not in db["notas"]:
        return jsonify({
            "status": "success",
            "data": []
        })

    matriz = db["notas"][codigo_curso]
    notas_estudiante = matriz.obtener_por_columna(carnet)

    return jsonify({
        "status": "success",
        "data": notas_estudiante
    })


@notas_bp.route("/tutor/reporte/promedio/<codigo_curso>", methods=["GET"])
def reporte_promedio(codigo_curso):
    if codigo_curso not in db["notas"]:
        return jsonify({
            "status": "success",
            "data": []
        })

    matriz = db["notas"][codigo_curso]
    registros = matriz.todos()

    acumulado = {}
    conteo = {}

    for r in registros:
        actividad = r["actividad"]
        nota = r["nota"]
        acumulado[actividad] = acumulado.get(actividad, 0) + nota
        conteo[actividad] = conteo.get(actividad, 0) + 1

    promedios = []
    for actividad in acumulado:
        promedios.append({
            "actividad": actividad,
            "promedio": round(acumulado[actividad] / conteo[actividad], 2)
        })

    return jsonify({
        "status": "success",
        "data": promedios
    })


@notas_bp.route("/tutor/reporte/top/<codigo_curso>/<actividad>", methods=["GET"])
def reporte_top(codigo_curso, actividad):
    if codigo_curso not in db["notas"]:
        return jsonify({
            "status": "success",
            "data": []
        })

    matriz = db["notas"][codigo_curso]
    registros = matriz.obtener_por_fila(actividad)
    registros_ordenados = sorted(registros, key=lambda x: x["nota"], reverse=True)

    return jsonify({
        "status": "success",
        "data": registros_ordenados
    })
