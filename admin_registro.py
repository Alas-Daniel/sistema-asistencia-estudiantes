import tkinter as tk
from tkinter import messagebox
from gestor_json import agregar_alumno
from generador_codigo import generar_credencial, imprimir_credencial

class RegistroAlumno(tk.Toplevel):
    def __init__(self, master, log_widget=None):
        super().__init__(master)
        self.title("Registrar Alumno")
        self.geometry("500x530")
        self.resizable(False, False)
        self.configure(bg="#D1D1D1")
        self.log_widget = log_widget
        self.master = master
        
        frame = tk.Frame(self, bg="#D1D1D1")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self, text="REGISTRAR ALUMNO", bg="#D1D1D1",
                 font=("Arial", 14, "bold")).pack(pady=55)
        
        tk.Label(frame, text="NIE:", bg="#D1D1D1", font=("Arial", 12)).pack(anchor="w")
        self.entry_nie = tk.Entry(frame, width=40, font=("Arial", 12))
        self.entry_nie.pack(pady=(5, 15))

        tk.Label(frame, text="Nombres:", bg="#D1D1D1", font=("Arial", 12)).pack(anchor="w")
        self.entry_nombres = tk.Entry(frame, width=40, font=("Arial", 12))
        self.entry_nombres.pack(pady=(5, 15))

        tk.Label(frame, text="Apellidos:", bg="#D1D1D1", font=("Arial", 12)).pack(anchor="w")
        self.entry_apellidos = tk.Entry(frame, width=40, font=("Arial", 12))
        self.entry_apellidos.pack(pady=(5, 25))

        btn_frame = tk.Frame(frame, bg="#D1D1D1")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Agregar", bg="#2DCA35", fg="black",
          font=("Arial", 11, "bold"),
          relief="flat", activebackground="#28A230", activeforeground="white",
          command=self.guardar_alumno).pack(side="left", fill="x", expand=True, padx=3)

        tk.Button(btn_frame, text="Limpiar", bg="#F0E113", fg="black",
          font=("Arial", 11, "bold"),
          relief="flat", activebackground="#E5D611", activeforeground="white",
          command=self.limpiar_campos).pack(side="left", fill="x", expand=True, padx=3)
        
        tk.Button(btn_frame, text="Regresar", bg="#DB1714", fg="black",
          font=("Arial", 11, "bold"),
          relief="flat", activebackground="#C21210", activeforeground="white",
          command=self.regresar).pack(side="left", fill="x", expand=True, padx=3)

    def guardar_alumno(self):
        nie = self.entry_nie.get().strip()
        nombres = self.entry_nombres.get().strip()
        apellidos = self.entry_apellidos.get().strip()

        if not nie or not nombres or not apellidos:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios.")
            return
        
        agregar_alumno(nie, nombres, apellidos)

        try:
            ruta_credencial = generar_credencial(nie, nombres, apellidos) #Generar
            imprimir_credencial(ruta_credencial) #Imprimir

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar o imprimir la credencial:\n{e}")
            return

        messagebox.showinfo("Éxito", f"Alumno {nombres} {apellidos} agregado correctamente.\nCredencial generada e impresa.")

        if self.log_widget:
            self.log_widget.insert(tk.END, f"Alumno agregado: {nie} | {nombres} {apellidos}\n")

        self.limpiar_campos()


    def limpiar_campos(self):
        self.entry_nie.delete(0, tk.END)
        self.entry_nombres.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)

    def regresar(self):
        self.destroy()
        if self.master:
            self.master.deiconify()