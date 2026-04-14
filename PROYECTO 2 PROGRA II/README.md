#  Proyecto 2 - API de Notas con Matriz Dispersa

##  Descripción
Este proyecto consiste en el desarrollo de una API en Python que permite la carga, almacenamiento y visualización de notas académicas utilizando una estructura de datos tipo matriz dispersa.

El sistema procesa archivos XML, almacena la información y genera reportes visuales en formato PDF.

---

##  Tecnologías utilizadas
- Python 3
- Flask
- Graphviz
- Postman
- XML

---

##  Estructura del Proyecto


---

##  Funcionalidades

✔ Cargar notas desde XML  
✔ Almacenar datos en matriz dispersa  
✔ Consultar datos mediante API REST  
✔ Generar reportes en PDF  

---

##  Endpoints de la API

###  Cargar Notas
- Método: POST  
- URL:  


- Ejemplo XML:

```xml
<?xml version="1.0"?>
<root>
    <notas>
        <actividad nombre="Tarea1" carnet="2021001">90</actividad>
        <actividad nombre="Tarea2" carnet="2021002">60</actividad>
        <actividad nombre="Tarea3" carnet="2021003">40</actividad>
    </notas>
</root>

 Ver Notas
Método: GET
http://127.0.0.1:5000/verNotas
 Generar Reporte
Método: GET
http://127.0.0.1:5000/reporte
 Generación de Reportes

}




