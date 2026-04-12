class NodoMatriz:
    def __init__(self, fila, columna, valor):
        self.fila = fila
        self.columna = columna
        self.valor = valor


class MatrizDispersa:
    def __init__(self):
        self.nodos = []

    def insertar(self, fila, columna, valor):
        for nodo in self.nodos:
            if nodo.fila == fila and nodo.columna == columna:
                nodo.valor = valor
                return
        self.nodos.append(NodoMatriz(fila, columna, valor))

    def obtener(self, fila, columna):
        for nodo in self.nodos:
            if nodo.fila == fila and nodo.columna == columna:
                return nodo.valor
        return None

    def obtener_por_fila(self, fila):
        resultado = []
        for nodo in self.nodos:
            if nodo.fila == fila:
                resultado.append({
                    "actividad": nodo.fila,
                    "carnet": nodo.columna,
                    "nota": nodo.valor
                })
        return resultado

    def obtener_por_columna(self, columna):
        resultado = []
        for nodo in self.nodos:
            if nodo.columna == columna:
                resultado.append({
                    "actividad": nodo.fila,
                    "carnet": nodo.columna,
                    "nota": nodo.valor
                })
        return resultado

    def todos(self):
        resultado = []
        for nodo in self.nodos:
            resultado.append({
                "actividad": nodo.fila,
                "carnet": nodo.columna,
                "nota": nodo.valor
            })
        return resultado
