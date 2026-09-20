import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Info del sistema ----------
NOMBRE_APP = "AUTOfactory - Sistema de Gestión Automotriz"
VERSION    = "1.0.0"
EMPRESA    = "Motores Eficientes S.A."
AUTOR      = "Brahyan Fernández Múnera"

# ============================================================
#  MÓDULO 1: VEHÍCULOS
# ============================================================
class FrameVehiculos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F7FA")
        self._construir()

    def _construir(self):
        # ---------- Título ----------
        tk.Label(self, text="Módulo de Vehículos",
                 font=("Segoe UI", 16, "bold"),
                 bg="#F5F7FA", fg="#2C3E50").pack(pady=(20, 10))

        # ---------- Frame contenedor del formulario ----------
        form = tk.Frame(self, bg="#F5F7FA")
        form.pack(pady=10)

        # ---------- Campo: Código ----------
        tk.Label(form, text="Código del modelo:",
                 font=("Segoe UI", 10), bg="#F5F7FA").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_codigo = tk.Entry(form, width=30, font=("Segoe UI", 10))
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)

        # ---------- Campo: Nombre ----------
        tk.Label(form, text="Nombre:",
                 font=("Segoe UI", 10), bg="#F5F7FA").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_nombre = tk.Entry(form, width=30, font=("Segoe UI", 10))
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        # ---------- Campo: Categoría (Combobox) ----------
        tk.Label(form, text="Categoría:",
                 font=("Segoe UI", 10), bg="#F5F7FA").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.combo_categoria = ttk.Combobox(form, width=27,
                                            values=["Sedan", "SUV", "Pickup"],
                                            state="readonly", font=("Segoe UI", 10))
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=2, column=1, padx=5, pady=5)

        # ---------- Campo: Contraseña (con show="*") ----------
        tk.Label(form, text="Clave de acceso:",
                 font=("Segoe UI", 10), bg="#F5F7FA").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_clave = tk.Entry(form, width=30, font=("Segoe UI", 10))
        self.entry_clave.config(show="*")   # ← OCULTA el texto
        self.entry_clave.grid(row=3, column=1, padx=5, pady=5)

        # ---------- Botones principales ----------
        botones = tk.Frame(self, bg="#F5F7FA")
        botones.pack(pady=15)

        tk.Button(botones, text="Guardar",
                  command=self.guardar,
                  font=("Segoe UI", 10, "bold"),
                  bg="#2E7D32", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=85)

        tk.Button(botones, text="Limpiar",
                  command=self.limpiar,
                  font=("Segoe UI", 10, "bold"),
                  bg="#C62828", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        # ---------- Tabla (Treeview) ----------
        cols = ("Código", "Nombre", "Categoría")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=6)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=180, anchor="center")
        self.tabla.pack(pady=15, padx=20, fill="x")

    # ------------------------------------------------------------
    #  MÉTODOS QUE DEMUESTRAN EL USO DE entry.get(), delete, insert
    # ------------------------------------------------------------

    def guardar(self):
        """Demuestra: entry.get()"""
        codigo = self.entry_codigo.get()      # ← LEER el contenido
        nombre = self.entry_nombre.get()
        categoria = self.combo_categoria.get()

        # Validación básica
        if not codigo or not nombre:
            messagebox.showwarning("Campos vacíos",
                "Debe ingresar código y nombre.")
            return

        # Insertar en la tabla
        self.tabla.insert("", "end", values=(codigo, nombre, categoria))
        messagebox.showinfo("Éxito",
            f"Vehículo registrado:\n\n"
            f"Código: {codigo}\n"
            f"Nombre: {nombre}\n"
            f"Categoría: {categoria}")

    def limpiar(self):
        """Demuestra: entry.delete(0, END)"""
        self.entry_codigo.delete(0, tk.END)   # ← BORRAR todo
        self.entry_nombre.delete(0, tk.END)
        self.entry_clave.delete(0, tk.END)
        self.combo_categoria.current(0)
        messagebox.showinfo("Limpiar", "Campos vaciados correctamente.")



# ============================================================
#  MÓDULO 2: PRODUCCIÓN — Formulario simple
# ============================================================
class FrameProduccion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F7FA")
        self._construir()

    def _construir(self):
        tk.Label(self, text="Módulo de Producción",
                 font=("Segoe UI", 16, "bold"),
                 bg="#F5F7FA", fg="#2C3E50").pack(pady=(20, 10))

        form = tk.Frame(self, bg="#F5F7FA")
        form.pack(pady=10)

        tk.Label(form, text="N° Orden:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.e_orden = tk.Entry(form, width=30)
        self.e_orden.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Cantidad:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.e_cantidad = tk.Entry(form, width=30)
        self.e_cantidad.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Registrar Orden",
                  command=self.registrar,
                  font=("Segoe UI", 10, "bold"),
                  bg="#2E7D32", fg="white",
                  width=18, relief="flat", cursor="hand2"
                  ).pack(pady=15)

    def registrar(self):
        orden = self.e_orden.get()
        cantidad = self.e_cantidad.get()
        if not orden or not cantidad:
            messagebox.showwarning("Validación", "Complete todos los campos.")
            return
        messagebox.showinfo("Éxito",
            f"Orden {orden} registrada con {cantidad} unidades.")
        self.e_orden.delete(0, tk.END)
        self.e_cantidad.delete(0, tk.END)

# ============================================================
#  MÓDULO 3: INVENTARIO
# ============================================================
class FrameInventario(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F7FA")
        self._construir()

    def _construir(self):
        tk.Label(self, text="Módulo de Inventario",
                 font=("Segoe UI", 16, "bold"),
                 bg="#F5F7FA", fg="#2C3E50").pack(pady=(20, 10))

        form = tk.Frame(self, bg="#F5F7FA")
        form.pack(pady=10)

        tk.Label(form, text="Código componente:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.e_cod = tk.Entry(form, width=30)
        self.e_cod.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Cantidad disponible:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.e_disp = tk.Entry(form, width=30)
        self.e_disp.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Stock mínimo:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.e_min = tk.Entry(form, width=30)
        self.e_min.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Verificar Stock",
                  command=self.verificar,
                  font=("Segoe UI", 10, "bold"),
                  bg="#F9A825", fg="white",
                  width=18, relief="flat", cursor="hand2"
                  ).pack(pady=15)

        self.lbl_alerta = tk.Label(self, text="", font=("Segoe UI", 11, "bold"),
                                   bg="#F5F7FA")
        self.lbl_alerta.pack(pady=5)

    def verificar(self):
        try:
            disp = int(self.e_disp.get())
            minimo = int(self.e_min.get())
        except ValueError:
            messagebox.showerror("Error", "Las cantidades deben ser numéricas.")
            return

        if disp <= minimo:
            self.lbl_alerta.config(text=f"⚠ ALERTA: Stock bajo ({disp} ≤ {minimo})",
                                   fg="#C62828")
        else:
            self.lbl_alerta.config(text=f"✔ Stock suficiente ({disp})",
                                   fg="#2E7D32")

# ============================================================
#  MÓDULO 4: EMPLEADOS
# ============================================================
class FrameEmpleados(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F7FA")
        self._construir()

    def _construir(self):
        tk.Label(self, text="Módulo de Gestión de Empleados",
                 font=("Segoe UI", 16, "bold"),
                 bg="#F5F7FA", fg="#2C3E50").pack(pady=(20, 10))

        form = tk.Frame(self, bg="#F5F7FA")
        form.pack(pady=10)

        tk.Label(form, text="N° Empleado:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.e_num = tk.Entry(form, width=30)
        self.e_num.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Nombres:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.e_nom = tk.Entry(form, width=30)
        self.e_nom.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Apellidos:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.e_ape = tk.Entry(form, width=30)
        self.e_ape.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Turno:", font=("Segoe UI", 10),
                 bg="#F5F7FA").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.c_turno = ttk.Combobox(form, width=27,
                                    values=["Mañana", "Tarde", "Noche"],
                                    state="readonly")
        self.c_turno.current(0)
        self.c_turno.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self, text="Registrar Empleado",
                  command=self.registrar,
                  font=("Segoe UI", 10, "bold"),
                  bg="#2E7D32", fg="white",
                  width=20, relief="flat", cursor="hand2"
                  ).pack(pady=15)

    def registrar(self):
        if not self.e_num.get() or not self.e_nom.get():
            messagebox.showwarning("Validación", "Complete los campos.")
            return
        messagebox.showinfo("Éxito",
            f"Empleado {self.e_nom.get()} {self.e_ape.get()} registrado.")

# ============================================================
#  VENTANA PRINCIPAL
# ============================================================
class AplicacionAutofactory(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{NOMBRE_APP} v{VERSION}")
        self.geometry("1200x750")
        self.configure(bg="#2C3E50")
        self.minsize(1050, 650)
        self._construir_ui()

    def _construir_ui(self):
        # ---------- Encabezado ----------
        header = tk.Frame(self, bg="#1B2A41", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🏭 Autofactory",
                 font=("Segoe UI", 22, "bold"),
                 bg="#1B2A41", fg="white").pack(side="left", padx=25, pady=15)

        tk.Label(header, text=EMPRESA,
                 font=("Segoe UI", 11),
                 bg="#1B2A41", fg="#B0BEC5").pack(side="left", pady=22)

        tk.Label(header, text=f"Usuario: {AUTOR}",
                 font=("Segoe UI", 10, "bold"),
                 bg="#1B2A41", fg="#F9A825").pack(side="right", padx=25)

        # ---------- Notebook (pestañas) ----------
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TNotebook", background="#2C3E50", borderwidth=0)
        estilo.configure("TNotebook.Tab",
                         font=("Segoe UI", 10, "bold"),
                         padding=[15, 8],
                         background="#34495E",
                         foreground="white")
        estilo.map("TNotebook.Tab",
                   background=[("selected", "#F5F7FA")],
                   foreground=[("selected", "#2C3E50")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Carga de los 4 módulos
        self.notebook.add(FrameVehiculos(self.notebook),  text="🚗 Vehículos")
        self.notebook.add(FrameProduccion(self.notebook), text="🏗️ Producción")
        self.notebook.add(FrameInventario(self.notebook), text="📦 Inventario")
        self.notebook.add(FrameEmpleados(self.notebook),  text="👷 Empleados")

        # ---------- Barra de estado ----------
        self.status = tk.Label(self, text="Sistema listo",
                               anchor="w", bg="#C62828", fg="white",
                               font=("Segoe UI", 9), padx=15)
        self.status.pack(fill="x", side="bottom")

# ---------- Inicialización del programa ----------
if __name__ == "__main__":
    app = AplicacionAutofactory()
    app.mainloop()