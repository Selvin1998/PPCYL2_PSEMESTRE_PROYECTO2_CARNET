import graphviz
import os
from backend.nodo import NodoInterno


class MatrizDispersa:
    def __init__(self):
        self.nodos = []

    def insertar(self, fila, columna, valor):
        nuevo = NodoInterno(fila, columna, valor)
        self.nodos.append(nuevo)

    def mostrar(self):
        print("---- DATOS DE LA MATRIZ ----")
        for nodo in self.nodos:
            print(f"Actividad: {nodo.fila} | Carnet: {nodo.columna} | Nota: {nodo.valor}")

    def generar_reporte(self):
        try:
            # Ruta de Graphviz (ajusta si es necesario)
            os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

            # Crear carpeta si no existe
            if not os.path.exists('reportes'):
                os.makedirs('reportes')

            dot = graphviz.Digraph(comment='Reporte de Notas', format='pdf')
            dot.attr(rankdir='TB')

            # 📊 Cálculos
            total = len(self.nodos)
            suma = sum(int(getattr(nodo, 'valor', 0)) for nodo in self.nodos)
            promedio = suma / total if total > 0 else 0

            # 🔵 Nodo principal
            dot.node(
                'R',
                f"REPORTE DE NOTAS\nTotal: {total}\nPromedio: {round(promedio, 2)}",
                shape='box',
                style='filled',
                fillcolor='lightblue'
            )

            # 🔄 Nodos dinámicos
            for nodo in self.nodos:
                id_act = f"A_{nodo.fila}"
                id_est = f"E_{nodo.columna}"
                id_nota = f"N_{nodo.fila}_{nodo.columna}"

                # 🟧 Actividad
                dot.node(
                    id_act,
                    nodo.fila,
                    shape='box',
                    style='filled',
                    fillcolor='orange'
                )

                # 🟩 Estudiante
                dot.node(
                    id_est,
                    str(nodo.columna),
                    shape='box',
                    style='filled',
                    fillcolor='green'
                )

                # 🟡 Nota
                dot.node(
                    id_nota,
                    str(getattr(nodo, 'valor', 0)),
                    shape='circle',
                    style='filled',
                    fillcolor='yellow'
                )

                # 🔗 Conexiones
                dot.edge('R', id_act)
                dot.edge(id_act, id_nota)
                dot.edge(id_est, id_nota)

            # 📄 Generar PDF
            dot.render('reportes/reporte_notas', view=True)

            print("✅ Reporte generado correctamente")

        except Exception as e:
            print("❌ Error al generar reporte:", e)

