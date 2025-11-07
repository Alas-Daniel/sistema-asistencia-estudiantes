from PIL import Image
from generador_codigo import generar_codigo

def imprimir_ticket(nombre, codigo):
    ruta = generar_codigo(nombre, codigo)
    print(f"Ticket generado: {ruta}")
    try:
        imagen = Image.open(ruta)
        imagen.show()
    except Exception as e:
        print("Error al abrir la imagen:", e)
