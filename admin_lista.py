import tkinter as tk
from tkinter import ttk, messagebox
from gestor_json import obtener_alumnos
from generador_codigo import generar_credencial, imprimir_credencial

class ListaAlumnos(tk.Toplevel):
    def __init__(self, master, log_widget=None):
        super().__init__(master)
        self.title("Lista de Alumnos")
        self.geometry("750x650")
        self.resizable(False, False)
        self.configure(bg="#D1D1D1")
        self.log_widget = log_widget

        tk.Label(self, text="ALUMNOS REGISTRADOS", bg="#D1D1D1",
                 font=("Arial", 14, "bold")).pack(pady=(55, 20))
        
        tk.Label(self, text="Lista de alumnos registrados en el sistema", bg="#D1D1D1",
                 font=("Arial", 13, "normal")).pack(pady=(0, 25))
        
        top_frame = tk.Frame(self, bg="#D1D1D1")
        top_frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Button(top_frame, text="Regresar", bg="#DB1714", fg="black",
                  font=("Arial", 11, "bold"),
                  relief="flat", activebackground="#C21210", activeforeground="white",
                  command=self.regresar).pack(side="right")

        tree_frame = tk.Frame(self, bg="#D1D1D1")
        tree_frame.pack(padx=20, pady=15, fill="both", expand=True)

        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")

        columnas = ("nie", "nombres", "apellidos", "generar")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )

        self.tree.heading("nie", text="NIE")
        self.tree.heading("nombres", text="Nombres")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("generar", text="Credencial")

        self.tree.column("nie", width=100, anchor="center")
        self.tree.column("nombres", width=200, anchor="w")
        self.tree.column("apellidos", width=200, anchor="w")
        self.tree.column("generar", width=100, anchor="center")

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<Button-1>", self.detectar_click)

        self.mostrar_alumnos()

    def mostrar_alumnos(self):
        alumnos = obtener_alumnos()
        for item in self.tree.get_children():
            self.tree.delete(item)

        for a in alumnos:
            nie = a.get("nie", "N/A")
            nombres = a.get("nombres", "")
            apellidos = a.get("apellidos", "")
            self.tree.insert("", "end", values=(nie, nombres, apellidos, "Generar"))

        if self.log_widget:
            self.log_widget.insert(tk.END, f"Se visualizó la lista de {len(alumnos)} alumnos.\n")

    def regresar(self):
        self.destroy()
        if self.master:
            self.master.deiconify()

    def detectar_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)

        if not item:
            return

        if column == "#4":
            valores = self.tree.item(item, "values")
            nie = valores[0]
            nombres = valores[1]
            apellidos = valores[2]

            try:
                foto_path = f"fotos/{nie}.jpg"
                ruta_guardada = generar_credencial(nie, nombres, apellidos, foto_path)
                imprimir_credencial(ruta_guardada)

                messagebox.showinfo(
                    "Éxito",
                    f"Credencial generada e impresa correctamente para:\n"
                    f"{nombres} {apellidos}\nNIE: {nie}"
                )

                if self.log_widget:
                    self.log_widget.insert(
                        tk.END,
                        f"Credencial generada e impresa para {nombres} {apellidos} (NIE: {nie})\n"
                        f"Archivo: {ruta_guardada}\n"
                    )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo generar o imprimir la credencial para {nombres} {apellidos}:\n{str(e)}"
                )
                if self.log_widget:
                    self.log_widget.insert(
                        tk.END,
                        f"Error al generar/imprimir credencial para {nombres} {apellidos}: {str(e)}\n"
                    )