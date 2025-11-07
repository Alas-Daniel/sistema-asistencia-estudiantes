# ui_admin.py
import tkinter as tk
from tkinter import scrolledtext
from admin_habilitar import HabilitarAsistencia
from admin_registro import RegistroAlumno
from admin_lista import ListaAlumnos
from admin_historial import HistorialAsistencias

class AdminApp(tk.Tk):
    def __init__(self, admin_name="Administrador"):
        super().__init__()
        self.title("Panel de Administración - Sistema de Asistencia")
        self.geometry("700x500")
        self.configure(bg="#F2F2F2")
        self.admin_name = admin_name

        tk.Label(
            self,
            text=f"Bienvenido, {self.admin_name}",
            bg="#F2F2F2",
            font=("Arial", 18, "bold"),
            fg="#000000"
        ).pack(pady=(20, 5))

        tk.Label(
            self,
            text="OPCIONES: ",
            bg="#F2F2F2",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))


        btn_style = {"font": ("Arial", 12), "width": 50, "height": 2, "relief": "flat"}

        tk.Button(self, text="Habilitar asistencia",
                  bg="#919191", command=self.abrir_habilitar, **btn_style).pack(pady=5)
        
        tk.Button(self, text="Registrar alumno",
                  bg="#919191", command=self.abrir_registro, **btn_style).pack(pady=5)

        tk.Button(self, text="Ver lista de alumnos",
                  bg="#919191", command=self.abrir_lista, **btn_style).pack(pady=5)

        tk.Button(self, text="Ver historial de asistencias",
                  bg="#919191", command=self.abrir_historial, **btn_style).pack(pady=5)

        tk.Button(
            self,
            text="Cerrar sesión",
            bg="#FF0000",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            command=self.cerrar_sesion
        ).pack(pady=10)

    def abrir_habilitar(self):
        self.withdraw() 
        HabilitarAsistencia(self)

    def abrir_registro(self):
        self.withdraw() 
        log_widget = getattr(self, "text_log", None)  
        RegistroAlumno(self, log_widget=log_widget)

    def abrir_lista(self):
        self.withdraw() 
        log_widget = getattr(self, "text_log", None)
        ListaAlumnos(self, log_widget=log_widget)

    def abrir_historial(self):
        self.withdraw() 
        log_widget = getattr(self, "text_log", None)
        HistorialAsistencias(self, log_widget=log_widget)

    def cerrar_sesion(self):
        self.withdraw()
        from ui_login import LoginApp
        app = LoginApp()
        app.mainloop()
