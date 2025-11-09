import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import gestor_json as db

class HabilitarAsistencia(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Habilitar Asistencia")
        self.geometry("850x650")
        self.resizable(False, False)
        self.configure(bg="#D1D1D1")

        tk.Label(self, text="ALUMNOS REGISTRADOS", bg="#D1D1D1",
                 font=("Arial", 14, "bold")).pack(pady=(30, 20))
        
        tk.Label(self, text="Pase su credencial en el escaner para marcar asistencia", bg="#D1D1D1",
                 font=("Arial", 13, "normal")).pack(pady=(0, 15))
        
        tk.Label(self, text="Hora de entrada: 7:00 am", bg="#D1D1D1",
                 font=("Arial", 13, "normal")).pack(pady=(0, 15))
        
        frame_entrada = tk.Frame(self, bg="#D1D1D1")
        frame_entrada.pack(pady=(0, 20))
        
        tk.Label(frame_entrada, text="Pase su credencial:", bg="#D1D1D1",
                 font=("Arial", 10, "normal")).pack(anchor="w", padx=5)
        
        self.entrada_codigo = tk.Entry(frame_entrada, font=("Courier New", 14, "bold"),
                               width=40, justify="center", bg="white",
                               relief="solid", borderwidth=2)

        self.entrada_codigo.pack(padx=5, pady=5)
        self.entrada_codigo.focus_force()
        self.entrada_codigo.bind("<Key>", self.bloquear_teclado)
        #self.entrada_codigo.bind("<Return>", self.procesar_codigo)
        self.entrada_codigo.bind("<KeyRelease>", self.detectar_fin_de_scan)
        self.after_id = None 

        frame_tabla = tk.Frame(self, bg="#D1D1D1")
        frame_tabla.pack(padx=40, pady=(0, 20), fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        # tabla
        self.tabla = ttk.Treeview(frame_tabla, 
                                   columns=("NIE", "Nombre", "Hora", "Estado"),
                                   show="headings",
                                   yscrollcommand=scrollbar.set,
                                   height=10)
        
        self.tabla.heading("NIE", text="NIE")
        self.tabla.heading("Nombre", text="Nombre Estudiante")
        self.tabla.heading("Hora", text="Hora")
        self.tabla.heading("Estado", text="Estado")
        
        self.tabla.column("NIE", width=100, anchor="w")
        self.tabla.column("Nombre", width=350, anchor="w")
        self.tabla.column("Hora", width=120, anchor="center")
        self.tabla.column("Estado", width=120, anchor="center")
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tabla.yview)
        
        self.tabla.tag_configure("a_tiempo", background="#d4edda")
        self.tabla.tag_configure("tarde", background="#fff3cd")
        self.tabla.tag_configure("muy_tarde", background="#f8d7da")
        
        
        frame_footer = tk.Frame(self, bg="#d9d9d9") # Frame footer
        frame_footer.pack(side="bottom", fill="x", padx=20, pady=(10, 20))
        
        self.hora_label = tk.Label(frame_footer, text="Hora Local: --:--:--", bg="#d9d9d9",
                                    font=("Arial", 10, "normal"))
        self.hora_label.pack(side="left", padx=(10, 20))
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        tk.Label(frame_footer, text=f"Fecha: {fecha_actual}", bg="#d9d9d9",
                 font=("Arial", 10, "normal")).pack(side="left")
        
        tk.Button(frame_footer, text="Generar PDF del día", bg="#4CAF50", fg="white",
          font=("Arial", 11, "bold"), relief="flat",
          activebackground="#45A049", activeforeground="white",
          command=self.generar_reporte_dia).pack(side="right", padx=10)

        tk.Button(frame_footer, text="Regresar", bg="#DB1714", fg="black", # Regresar
                  font=("Arial", 11, "bold"),
                  relief="flat", activebackground="#C21210", activeforeground="white",
                  command=self.regresar).pack(side="right", padx=10)
        
        self.actualizar_hora()
        self.cargar_asistencias_del_dia()

    def generar_reporte_dia(self):
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        ruta_pdf = db.generar_pdf_asistencias_dia(fecha_actual)
        if ruta_pdf:
            messagebox.showinfo("Éxito", f"Reporte generado correctamente:\n{ruta_pdf}")
        else:
            messagebox.showwarning("Sin registros", "No hay asistencias registradas para hoy.")

    def actualizar_hora(self):
        hora_actual = datetime.now().strftime("%H:%M:%S")
        self.hora_label.config(text=f"Hora Local: {hora_actual}")
        self.after(1000, self.actualizar_hora)
        
    def cargar_asistencias_del_dia(self): #Mostrar asistencias
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        asistencias = db.obtener_asistencias_por_fecha(fecha_actual)

        for asistencia in asistencias:
            if asistencia["estado"] == "A tiempo":
                tag = "a_tiempo"
            elif asistencia["estado"] == "Tarde":
                tag = "tarde"
            else:
                tag = "muy_tarde"

            nombre_completo = f"{asistencia['nombres']} {asistencia['apellidos']}"
            self.tabla.insert("", 0, values=(
                asistencia["nie"],
                nombre_completo,
                asistencia["hora"],
                asistencia["estado"]
            ), tags=(tag,))

    
    def procesar_codigo(self, event):
        codigo = self.entrada_codigo.get().strip()
        
        if not codigo:
            return
        alumno = db.buscar_alumno_por_nie(codigo)
        
        if alumno:
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            
            if db.ya_registro_hoy(codigo, fecha_actual): # verificar si ya registró ho
                messagebox.showwarning("Advertencia", 
                                      f"{alumno['nombres']} {alumno['apellidos']} ya registró asistencia hoy")
                self.entrada_codigo.delete(0, tk.END)
                return
            
            hora_actual = datetime.now()
            estado = self.calcular_estado(hora_actual)
            
            db.registrar_asistencia(
                alumno['nie'],
                alumno['nombres'],
                alumno['apellidos'],
                fecha_actual,
                hora_actual.strftime("%H:%M:%S"),
                estado
            )
            self.agregar_registro(alumno, hora_actual, estado)
            
        else:
            messagebox.showerror("Error", "Credencial no encontrada")
        
        self.entrada_codigo.delete(0, tk.END)
    
    def calcular_estado(self, hora):
        hora_limite = hora.replace(hour=7, minute=0, second=0)
        
        if hora <= hora_limite:
            return "A tiempo"
        elif hora <= hora_limite.replace(minute=15):
            return "Tarde"
        else:
            return "Muy tarde"
    
    def agregar_registro(self, alumno, hora, estado):
        if estado == "A tiempo":
            tag = "a_tiempo"
        elif estado == "Tarde":
            tag = "tarde"
        else:
            tag = "muy_tarde"
        
        nombre_completo = f"{alumno['nombres']} {alumno['apellidos']}"
        self.tabla.insert("", 0, values=(
            alumno['nie'],
            nombre_completo,
            hora.strftime("%H:%M:%S"),
            estado
        ), tags=(tag,))
        
        self.bell()
    
    def bloquear_teclado(self, event):
        if event.keysym in ("Return", "Tab"):
            return  
        if len(event.char) == 1 and event.char.isprintable():
            if event.keycode != 0 and not event.state & 0x0004:
                return  

    def detectar_fin_de_scan(self, event):
        if self.after_id:
            self.after_cancel(self.after_id)
        
        self.after_id = self.after(200, self.procesar_si_completo)

    def procesar_si_completo(self):
        codigo = self.entrada_codigo.get().strip()
        if codigo:
            self.procesar_codigo(None)

    def regresar(self):
        self.destroy()
        if self.master:
            self.master.deiconify()
