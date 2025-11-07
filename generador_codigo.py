import os
from PIL import Image, ImageDraw, ImageFont, ImageWin
import barcode
from barcode.writer import ImageWriter
import win32print
import win32ui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODES_DIR = os.path.join(BASE_DIR, "codigos")
CRED_DIR = os.path.join(BASE_DIR, "credenciales")

os.makedirs(CODES_DIR, exist_ok=True)
os.makedirs(CRED_DIR, exist_ok=True)

def generar_codigo(nombre_archivo, codigo):
    tipo = barcode.get_barcode_class("code128")
    
    writer = ImageWriter()
    
    ruta_base = os.path.join(CODES_DIR, nombre_archivo)
    codigo_barra = tipo(str(codigo), writer=writer)
    ruta_generada = codigo_barra.save(ruta_base, options={"write_text": False})
    
    return os.path.abspath(ruta_generada)


def medir_texto(draw, texto, font):
    if hasattr(draw, "textbbox"):  # Pillow >=10
        x0, y0, x1, y1 = draw.textbbox((0, 0), texto, font=font)
        return x1 - x0, y1 - y0
    else:
        return draw.textsize(texto, font=font)


def generar_credencial(nie, nombres, apellidos, foto_path=None):
    nombre_archivo = f"{nie}_{nombres.replace(' ', '_')}_{apellidos.replace(' ', '_')}"
    ruta_codigo = generar_codigo(nombre_archivo, nie)

    ANCHO = 420
    ALTO = 700
    fondo_color = (255, 255, 255)

    carnet = Image.new("RGB", (ANCHO, ALTO), color=fondo_color)
    draw = ImageDraw.Draw(carnet)

    try:
        font_titulo = ImageFont.truetype("arialbd.ttf", 26)
        font_texto = ImageFont.truetype("arial.ttf", 22)
        font_peq = ImageFont.truetype("arial.ttf", 18)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()
        font_peq = ImageFont.load_default()

    y = 10

    titulo = "CREDENCIAL ESTUDIANTIL"
    tw, th = medir_texto(draw, titulo, font_titulo)
    draw.text(((ANCHO - tw) / 2, y), titulo, fill="black", font=font_titulo)
    y += th + 10
    draw.line([(0, y), (ANCHO, y)], fill="black", width=2)
    y += 10

    if foto_path and os.path.exists(foto_path):
        foto = Image.open(foto_path).resize((150, 150))
    else:

        generic_path = os.path.join(BASE_DIR, "sources", "usuario_credencial.jpg")
        if os.path.exists(generic_path):
            foto = Image.open(generic_path).resize((150, 150))
        else:
        
            foto = Image.new("RGB", (150, 150), color=(220, 220, 220))
    carnet.paste(foto, ((ANCHO - 150) // 2, y))
    y += 160



    draw.text((20, y), f"NIE: {nie}", fill="black", font=font_texto)
    y += 35
    draw.text((20, y), f"Nombres: {nombres}", fill="black", font=font_texto)
    y += 35
    draw.text((20, y), f"Apellidos: {apellidos}", fill="black", font=font_texto)
    y += 40

    draw.line([(0, y), (ANCHO, y)], fill="black", width=2)
    y += 10

    if os.path.exists(ruta_codigo):
        codigo_img = Image.open(ruta_codigo).resize((380, 100))
        carnet.paste(codigo_img, ((ANCHO - 380) // 2, y))
        y += 110

    draw.line([(0, y), (ANCHO, y)], fill="black", width=1)
    y += 10
    pie_texto = "ESTUDIANTE"
    tw, _ = medir_texto(draw, pie_texto, font_peq)
    draw.text(((ANCHO - tw) / 2, y), pie_texto, fill="black", font=font_peq)

    ruta_final = os.path.join(CRED_DIR, f"{nombre_archivo}_ticket.png")
    carnet = carnet.crop((0, 0, ANCHO, y + 60))
    carnet.save(ruta_final)

    return os.path.abspath(ruta_final)


def imprimir_credencial(ruta_credencial, impresora=None):
    if impresora is None:
        impresora = win32print.GetDefaultPrinter()

    hprinter = win32print.OpenPrinter(impresora)
    pdc = win32ui.CreateDC()
    pdc.CreatePrinterDC(impresora)
    pdc.StartDoc("Impresión Automática de Credencial")
    pdc.StartPage()

    img = Image.open(ruta_credencial)
    dib = ImageWin.Dib(img)

    dib.draw(pdc.GetHandleOutput(), (0, 0, img.width, img.height))

    pdc.EndPage()
    pdc.EndDoc()
    pdc.DeleteDC()


if __name__ == "__main__":
    print("Ejemplo: función lista para usar desde interfaz.")
