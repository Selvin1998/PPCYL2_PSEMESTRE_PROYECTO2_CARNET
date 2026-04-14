class NodoInterno:
    def __init__(self, fila, columna, valor):
        self.fila = fila        # Ej: Tarea1
        self.columna = columna  # Ej: 2021001
        self.valor = valor      # Ej: 85

        # Apuntadores (para matriz dispersa después)
        self.derecha = None
        self.abajo = None


