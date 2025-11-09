import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
CODIGOS_DIR = os.path.join(BASE_DIR, "codigos")
ASISTENCIAS_DIR = os.path.join(DATA_DIR, "asistencias")

RUTA_ALUMNOS = os.path.join(DATA_DIR, "alumnos.json")
RUTA_USUARIOS = os.path.join(DATA_DIR, "usuarios.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(CODIGOS_DIR, exist_ok=True)
os.makedirs(ASISTENCIAS_DIR, exist_ok=True)

def cargar_datos(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_datos(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def agregar_alumno(nie, nombres, apellidos):
    alumnos = cargar_datos(RUTA_ALUMNOS)
    
    for alumno in alumnos: #Validacion del nie
        if alumno.get("nie") == nie:
            return False
        
    alumno = {"nie": nie, "nombres": nombres, "apellidos": apellidos}
    alumnos.append(alumno)
    guardar_datos(RUTA_ALUMNOS, alumnos)
    return True

def obtener_alumnos():
    return cargar_datos(RUTA_ALUMNOS)

def buscar_alumno_por_nie(nie):
    alumnos = cargar_datos(RUTA_ALUMNOS)
    for alumno in alumnos:
        if alumno.get("nie") == nie:
            return alumno
    return None

def obtener_ruta_asistencias_por_materia(materia):
    if not materia:
        materia = "general"
    materia = materia.lower().replace(" ", "_")
    return os.path.join(ASISTENCIAS_DIR, f"{materia}.json")

def registrar_asistencia(nie, nombres, apellidos, fecha, hora, estado, materia):
    ruta_asistencia = obtener_ruta_asistencias_por_materia(materia)
    asistencias = cargar_datos(ruta_asistencia)
    asistencia = {
        "nie": nie,
        "nombres": nombres,
        "apellidos": apellidos,
        "fecha": fecha,
        "hora": hora,
        "estado": estado
    }
    asistencias.append(asistencia)
    guardar_datos(ruta_asistencia, asistencias)

def ya_registro_hoy(nie, fecha, materia):
    ruta_asistencia = obtener_ruta_asistencias_por_materia(materia)
    asistencias = cargar_datos(ruta_asistencia)
    for asistencia in asistencias:
        if asistencia.get("nie") == nie and asistencia.get("fecha") == fecha:
            return True
    return False

def obtener_asistencias(materia):
    ruta_asistencia = obtener_ruta_asistencias_por_materia(materia)
    return cargar_datos(ruta_asistencia)

def obtener_asistencias_por_fecha(fecha, materia):
    asistencias = obtener_asistencias(materia)
    return [a for a in asistencias if a.get("fecha") == fecha]

def validar_usuario(usuario, password, rol=None):
    if not os.path.exists(RUTA_USUARIOS):
        return None

    usuarios = cargar_datos(RUTA_USUARIOS)
    for u in usuarios:
        if u.get("usuario") == usuario and u.get("password") == password:
            if rol and u.get("rol") != rol:
                return None
            return u
    return None

#Archivos pdf
def generar_pdf_asistencia(nie, materia):
    alumno = buscar_alumno_por_nie(nie)
    if not alumno:
        return None

    ruta_asistencia = obtener_ruta_asistencias_por_materia(materia)
    asistencias = [a for a in cargar_datos(ruta_asistencia) if a.get("nie") == nie]
    if not asistencias:
        return None

    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_pdf = f"{nie}_{materia}_{fecha_actual}.pdf"
    ruta_pdf = os.path.join(PDF_DIR, nombre_pdf)

    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter,
                            leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph(f"REPORTE DE ASISTENCIA - {materia.capitalize()}", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>NIE:</b> {nie}", styles["Normal"]))
    story.append(Paragraph(f"<b>Nombre:</b> {alumno['nombres']} {alumno['apellidos']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    data = [["Fecha", "Hora", "Estado"]]
    for a in asistencias:
        data.append([a["fecha"], a["hora"], a["estado"]])

    table = Table(data, colWidths=[150, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d3d3d3")),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    story.append(table)

    doc.build(story)
    return ruta_pdf

def generar_pdf_asistencias_dia(fecha, materia):
    ruta_asistencia = obtener_ruta_asistencias_por_materia(materia)
    asistencias = cargar_datos(ruta_asistencia)
    asistencias_dia = [a for a in asistencias if a.get("fecha") == fecha]

    if not asistencias_dia:
        return None

    fecha_nombre = fecha.replace("/", "-")
    nombre_pdf = f"asistencias_{materia}_{fecha_nombre}.pdf"
    ruta_pdf = os.path.join(PDF_DIR, nombre_pdf)

    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter,
                            leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph(f"REPORTE DE ASISTENCIAS DEL DÍA - {materia.capitalize()}", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Fecha:</b> {fecha}", styles["Normal"]))
    story.append(Spacer(1, 12))

    data = [["NIE", "Nombre", "Hora", "Estado"]]
    for a in asistencias_dia:
        nombre_completo = f"{a['nombres']} {a['apellidos']}"
        data.append([a["nie"], nombre_completo, a["hora"], a["estado"]])

    table = Table(data, colWidths=[100, 200, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d3d3d3")),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Generado desde el sistema de asistencia", styles["Normal"]))

    doc.build(story)
    return ruta_pdf
