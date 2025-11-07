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

RUTA_ALUMNOS = os.path.join(DATA_DIR, "alumnos.json")
RUTA_ASISTENCIAS = os.path.join(DATA_DIR, "asistencias.json")
RUTA_USUARIOS = os.path.join(DATA_DIR, "usuarios.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(CODIGOS_DIR, exist_ok=True)


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
    alumno = {"nie": nie, "nombres": nombres, "apellidos": apellidos}
    alumnos.append(alumno)
    guardar_datos(RUTA_ALUMNOS, alumnos)

def obtener_alumnos():
    return cargar_datos(RUTA_ALUMNOS)

def buscar_alumno_por_nie(nie):
    alumnos = cargar_datos(RUTA_ALUMNOS)
    for alumno in alumnos:
        if alumno.get("nie") == nie:
            return alumno
    return None

def registrar_asistencia(nie, nombres, apellidos, fecha, hora, estado):
    asistencias = cargar_datos(RUTA_ASISTENCIAS)
    asistencia = {
        "nie": nie,
        "nombres": nombres,
        "apellidos": apellidos,
        "fecha": fecha,
        "hora": hora,
        "estado": estado
    }
    asistencias.append(asistencia)
    guardar_datos(RUTA_ASISTENCIAS, asistencias)


def ya_registro_hoy(nie, fecha):
    asistencias = cargar_datos(RUTA_ASISTENCIAS)
    for asistencia in asistencias:
        if asistencia.get("nie") == nie and asistencia.get("fecha") == fecha:
            return True
    return False

def obtener_asistencias():
    return cargar_datos(RUTA_ASISTENCIAS)

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

def generar_pdf_asistencia(nie):
    alumno = buscar_alumno_por_nie(nie)
    if not alumno:
        return None

    asistencias = [a for a in cargar_datos(RUTA_ASISTENCIAS) if a.get("nie") == nie]
    if not asistencias:
        return None

    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_pdf = f"{nie}_{fecha_actual}.pdf"
    ruta_pdf = os.path.join(PDF_DIR, nombre_pdf)

    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter,
                            leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph("REPORTE DE ASISTENCIA", styles["Title"]))
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