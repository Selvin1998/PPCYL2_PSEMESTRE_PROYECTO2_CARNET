from django.shortcuts import render, redirect
import requests

# -------------------------
# LOGIN
# -------------------------
def login_view(request):
    mensaje = ""

    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                json={
                    "usuario": usuario,
                    "password": password
                }
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("mensaje") == "Login correcto":
                    tipo = data.get("tipo")

                    if tipo == "admin":
                        return redirect("panel_admin")

                    elif tipo == "tutor":
                        return redirect("panel_tutor")

                    elif tipo == "estudiante":
                        return redirect("panel_estudiante")

                else:
                    mensaje = "Credenciales incorrectas"
            else:
                mensaje = "Error en el servidor"

        except Exception as e:
            mensaje = "No se pudo conectar con el backend Flask"

    return render(request, "webapp/login.html", {"mensaje": mensaje})


# -------------------------
# PANELES
# -------------------------
def panel_admin(request):
    return render(request, "webapp/admin.html")


def panel_tutor(request):
    return render(request, "webapp/tutor.html")


def panel_estudiante(request):
    return render(request, "webapp/estudiante.html")


# -------------------------
# CARGAR CONFIGURACION (ADMIN)
# -------------------------
def cargar_config(request):
    if request.method == "POST":
        xml = request.POST.get("xml")

        try:
            requests.post(
                "http://127.0.0.1:5000/cargarConfiguracion",
                data=xml,
                headers={"Content-Type": "application/xml"}
            )
        except:
            pass

        return redirect("panel_admin")


# -------------------------
# CARGAR NOTAS (TUTOR)
# -------------------------
def cargar_xml(request):
    if request.method == "POST":
        xml = request.POST.get("xml")

        try:
            requests.post(
                "http://127.0.0.1:5000/cargarNotas",
                data=xml,
                headers={"Content-Type": "application/xml"}
            )
        except:
            pass

        return redirect("panel_tutor")


# -------------------------
# VER NOTAS
# -------------------------
def ver_notas(request):
    notas = []

    try:
        response = requests.get("http://127.0.0.1:5000/verNotas")
        data = response.json()
        notas = data.get("notas", [])
    except:
        notas = []

    return render(request, "webapp/notas.html", {"notas": notas})


# -------------------------
# GRAFICO
# -------------------------
def grafico(request):
    import requests

    datos = []

    try:
        response = requests.get("http://127.0.0.1:5000/grafico")
        datos = response.json()
    except:
        pass

    return render(request, "webapp/grafico.html", {"datos": datos})


# -------------------------
# REPORTE
# -------------------------
def generar_reporte(request):
    try:
        requests.get("http://127.0.0.1:5000/reporte")
    except:
        pass

    return redirect("panel_admin")