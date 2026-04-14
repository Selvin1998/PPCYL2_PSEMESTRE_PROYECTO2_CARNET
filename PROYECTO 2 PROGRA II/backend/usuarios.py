class SistemaUsuarios:

    def __init__(self):
        self.usuarios = []

    def agregar_usuario(self, usuario, password, tipo):
        self.usuarios.append({
            "usuario": usuario,
            "password": password,
            "tipo": tipo
        })

    def login(self, usuario, password):
        for u in self.usuarios:
            if u["usuario"] == usuario and u["password"] == password:
                return {
                    "mensaje": "Login correcto",
                    "tipo": u["tipo"]
                }
        return {"mensaje": "Credenciales incorrectas"}