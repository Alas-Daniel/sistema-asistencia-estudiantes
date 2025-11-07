import tkinter as tk
from tkinter import ttk, messagebox
from gestor_json import obtener_asistencias
from generar_pdf import generar_pdf_historial

class HistorialAsistencias(tk.Toplevel):
    def __init__(self, master, log_widget=None):
        super().__init__(master)
        self.title("Historial de Asistencias")
        self.geometry("850x650")
        self.configure(bg="#D1D1D1")
        self.resizable(False, False)
        self.log_widget = log_widget

        tk.Label(self, text="HISTORIAL DE ASISTENCIAS", font=("Arial",14,"bold"), bg="#D1D1D1").pack(pady=10)

        filtro_frame = tk.Frame(self, bg="#D1D1D1")
        filtro_frame.pack(pady=5)

        tk.Label(filtro_frame, text="Buscar por NIE:", bg="#D1D1D1").grid(row=0,column=0,padx=5)
        self.entry_nie = tk.Entry(filtro_frame)
        self.entry_nie.grid(row=0,column=1,padx=5)

        tk.Button(filtro_frame, text="Buscar", bg="#4CAF50", fg="white", relief="flat",
                  command=self.buscar_por_nie).grid(row=0,column=2,padx=5)
        tk.Button(filtro_frame, text="Mostrar todo", bg="#2196F3", fg="white", relief="flat",
                  command=self.mostrar_todo).grid(row=0,column=3,padx=5)
        tk.Button(filtro_frame, text="Exportar PDF", bg="#FF9800", fg="white", relief="flat",
                  command=self.exportar_pdf).grid(row=0,column=4,padx=5)
        tk.Button(filtro_frame, text="Regresar", bg="#DB1714", fg="white", relief="flat",
                  command=self.regresar).grid(row=0,column=5,padx=5)

        tree_frame = tk.Frame(self, bg="#D1D1D1")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("nie","nombres","apellidos","fecha","hora","estado")
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=130)
        self.tree.pack(fill="both", expand=True)

        self.asistencias = []
        self.mostrar_todo()

    def mostrar_todo(self):
        self.asistencias = obtener_asistencias()
        self.mostrar_asistencias(self.asistencias)

    def mostrar_asistencias(self, lista):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for a in lista:
            self.tree.insert("", "end", values=(a.get("nie","N/A"), a.get("nombres","Desconocido"),
                                                a.get("apellidos","Desconocido"), a.get("fecha",""),
                                                a.get("hora",""), a.get("estado","")))
        if self.log_widget:
            self.log_widget.insert(tk.END, f"Se visualizaron {len(lista)} registros.\n")

    def buscar_por_nie(self):
        nie = self.entry_nie.get().strip()
        if not nie:
            messagebox.showwarning("Campo vacío","Ingrese un NIE para buscar")
            return
        resultados = [a for a in self.asistencias if a.get("nie")==nie]
        if not resultados:
            messagebox.showinfo("Sin resultados",f"No se encontraron asistencias para el NIE {nie}")
        self.mostrar_asistencias(resultados)

    def exportar_pdf(self):
        nie = self.entry_nie.get().strip()
        if not nie:
            messagebox.showwarning("Campo vacío", "Ingrese un NIE para exportar el historial.")
            return

        alumno = next((a for a in self.asistencias if a.get("nie") == nie), None)
        if not alumno:
            messagebox.showinfo("No encontrado", f"No se encontraron datos para el NIE {nie}.")
            return

        asistencias_filtradas = [a for a in self.asistencias if a.get("nie") == nie]
        if not asistencias_filtradas:
            messagebox.showinfo("Sin datos", "No hay asistencias para exportar.")
            return

        ruta = generar_pdf_historial(alumno, asistencias_filtradas)
        messagebox.showinfo("PDF generado", f"El PDF fue guardado en:\n{ruta}")

    def regresar(self):
        self.destroy()
        if self.master:
            self.master.deiconify()
