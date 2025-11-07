import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generar_pdf_historial(alumno, asistencias):
    carpeta = "pdfs"
    os.makedirs(carpeta, exist_ok=True)

    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"{alumno['nie']}_{fecha_actual}.pdf"
    ruta_pdf = os.path.join(carpeta, nombre_archivo)

    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    contenido = []

    titulo = Paragraph("Historial de Asistencias", styles["Title"])
    contenido.append(titulo)
    contenido.append(Spacer(1, 0.3 * inch))

    datos_alumno = f"""
    <b>NIE:</b> {alumno['nie']}<br/>
    <b>Nombre:</b> {alumno['nombres']} {alumno['apellidos']}<br/>
    <b>Fecha de generación:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    """
    contenido.append(Paragraph(datos_alumno, styles["Normal"]))
    contenido.append(Spacer(1, 0.3 * inch))

    encabezados = ["Fecha", "Hora", "Estado"]
    datos_tabla = [encabezados]
    for a in asistencias:
        datos_tabla.append([a["fecha"], a["hora"], a["estado"]])

    tabla = Table(datos_tabla, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#B0BEC5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    contenido.append(tabla)

    doc.build(contenido)
    return os.path.abspath(ruta_pdf)
