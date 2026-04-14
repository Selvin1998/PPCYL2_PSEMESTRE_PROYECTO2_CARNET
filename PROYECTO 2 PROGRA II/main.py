import xml.etree.ElementTree as ET
from backend.matriz import MatrizDispersa

m = MatrizDispersa()

tree = ET.parse('data/notas.xml')
root = tree.getroot()

notas = root.find('notas')

for actividad in notas.findall('actividad'):
    nombre = actividad.get('nombre')
    carnet = actividad.get('carnet')
    valor = int(actividad.text)

    m.insertar(nombre, carnet, valor)

m.mostrar()

import xml.etree.ElementTree as ET

def generar_xml_salida():
    root = ET.Element("configuraciones_aplicadas")

    ET.SubElement(root, "tutores_cargados").text = "3"
    ET.SubElement(root, "estudiantes_cargados").text = "5"

    asignaciones = ET.SubElement(root, "asignaciones")

    tutores = ET.SubElement(asignaciones, "tutores")
    ET.SubElement(tutores, "total").text = "3"
    ET.SubElement(tutores, "correcto").text = "2"
    ET.SubElement(tutores, "incorrecto").text = "1"

    estudiantes = ET.SubElement(asignaciones, "estudiantes")
    ET.SubElement(estudiantes, "total").text = "5"
    ET.SubElement(estudiantes, "correcto").text = "4"
    ET.SubElement(estudiantes, "incorrecto").text = "1"

    tree = ET.ElementTree(root)
    tree.write("reportes/salida.xml", encoding="utf-8", xml_declaration=True)

    print("XML de salida generado.")

# LLAMAR FUNCIÓN
generar_xml_salida()