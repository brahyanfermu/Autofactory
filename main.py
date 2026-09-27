"""
AUTOfactory - Sistema de Gestión Automotriz
Ventana principal con las 4 pestañas.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from config import (NOMBRE_APP, VERSION, EMPRESA, AUTOR, TEMA_CLARO)
from conexion_bd import ConexionBD

# Importación de los módulos (pestañas)
from modulos.mod_vehiculos  import FrameVehiculos
from modulos.mod_produccion import FrameProduccion
from modulos.mod_inventario import FrameInventario
from modulos.mod_empleados  import FrameEmpleados


class AplicacionAutofactory(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{NOMBRE_APP} v{VERSION}")
        self.geometry("1200x750")
        self.configure(bg=TEMA_CLARO["fondo"])
        self.minsize(1050, 650)

        # Conexión a BD (Singleton)
        self.bd = ConexionBD()
        self.bd.conectar()
        estado_bd = "Conectada" if self.bd.esta_conectado() else "Sin conexión"

        self._construir_ui(estado_bd)

    # ------------------------------------------------------------
    def _construir_ui(self, estado_bd):
        # ---------- Encabezado ----------
        header = tk.Frame(self, bg=TEMA_CLARO["fondo_header"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🏭 Autofactory",
                 font=("Segoe UI", 22, "bold"),
                 bg=TEMA_CLARO["fondo_header"], fg="white"
                 ).pack(side="left", padx=25, pady=15)

        tk.Label(header, text=EMPRESA,
                 font=("Segoe UI", 11),
                 bg=TEMA_CLARO["fondo_header"], fg="#B0BEC5"
                 ).pack(side="left", pady=22)

        # Estado de conexión a BD
        color_bd = "#2E7D32" if estado_bd == "Conectada" else "#C62828"
        tk.Label(header, text=f"BD: {estado_bd}",
                 font=("Segoe UI", 10, "bold"),
                 bg=TEMA_CLARO["fondo_header"], fg=color_bd
                 ).pack(side="right", padx=10)

        tk.Label(header, text=f"Usuario: {AUTOR}",
                 font=("Segoe UI", 10, "bold"),
                 bg=TEMA_CLARO["fondo_header"], fg="#F9A825"
                 ).pack(side="right", padx=10)

        # ---------- Notebook (pestañas) ----------
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TNotebook",
                         background=TEMA_CLARO["texto"],
                         borderwidth=0)
        estilo.configure("TNotebook.Tab",
                         font=("Segoe UI", 10, "bold"),
                         padding=[15, 8],
                         background=TEMA_CLARO["tab_inactivo"],
                         foreground="white")
        estilo.map("TNotebook.Tab",
                   background=[("selected", TEMA_CLARO["tab_activo"])],
                   foreground=[("selected", TEMA_CLARO["texto"])])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Carga de los 4 módulos
        self.notebook.add(FrameVehiculos(self.notebook),  text="🚗 Vehículos")
        self.notebook.add(FrameProduccion(self.notebook), text="🏗️ Producción")
        self.notebook.add(FrameInventario(self.notebook), text="📦 Inventario")
        self.notebook.add(FrameEmpleados(self.notebook),  text="👷 Empleados")

        # ---------- Barra de estado ----------
        self.status = tk.Label(
            self,
            text=f"Sistema listo  |  Base de datos: {'OK' if estado_bd == 'Conectada' else 'ERROR'}",
            anchor="w", bg=TEMA_CLARO["fondo_status"], fg="white",
            font=("Segoe UI", 9), padx=15
        )
        self.status.pack(fill="x", side="bottom")

    # ------------------------------------------------------------
    def on_close(self):
        if messagebox.askokcancel("Salir", "¿Cerrar AUTOfactory?"):
            self.bd.cerrar()
            self.destroy()


# ---------- Inicialización del programa ----------
if __name__ == "__main__":
    app = AplicacionAutofactory()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()