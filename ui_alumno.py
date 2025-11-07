import tkinter as tk
from tkinter import messagebox
from gestor_json import registrar_asistencia
from datetime import datetime

class AlumnoApp(tk.Tk):
    def __init__(self, codigo):
        super().__init__()
        self.codigo = codigo
        self.title("Alumno - Marcar Asistencia")
        self.state('zoomed')  
        tk.Label(self, text=f"Bienvenido, {self.codigo}", font=("Arial", 12, "bold")).pack(pady=20)
        tk.Button(self, text="Marcar asistencia", command=self.marcar_asistencia).pack(pady=20)
        self.mainloop()

    def marcar_asistencia(self):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registrar_asistencia(self.codigo, fecha)
        messagebox.showinfo("Éxito", f"Asistencia registrada: {fecha}")
