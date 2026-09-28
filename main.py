"""
AUTOfactory - Sistema de Gestión Automotriz
Ventana principal con las 4 pestañas y cambio de tema.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from config import NOMBRE_APP, VERSION, EMPRESA, AUTOR
from conexion_bd import ConexionBD

# Importación del sistema de temas
from utils.temas import (obtener_tema, alternar_tema,
                         obtener_nombre_tema, aplicar_tema_ventana)

# ============================================================
#  MÓDULO VEHÍCULOS (MVC)
# ============================================================
from vistas.vista_vehiculos import VistaVehiculos
from vistas.vista_produccion import VistaProduccion
from vistas.vista_inventario import VistaInventario
from vistas.vista_empleados import VistaEmpleados


class AplicacionAutofactory(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{NOMBRE_APP} v{VERSION}")

        # ---------- Tamaño adaptativo a la pantalla ----------
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        ancho_ventana = int(ancho_pantalla * 0.90)
        alto_ventana = int(alto_pantalla * 0.90)

        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.minsize(1000, 650)

        # ---------- Favicon ----------
        try:
            if sys.platform.startswith("win"):
                self.iconbitmap("assets/icono.ico")
                print("[INFO] Favicon .ico cargado (Windows)")
            else:
                ruta_icono = "assets/icono_grande.png"
                if not os.path.exists(ruta_icono):
                    ruta_icono = "assets/icono.png"

                icono = tk.PhotoImage(file=ruta_icono)
                self.iconphoto(True, icono)
                self.icono_ref = icono
                print(f"[INFO] Favicon cargado desde: {ruta_icono}")
        except Exception as e:
            print(f"[INFO] No se pudo cargar el favicon: {e}")

        # ---------- Tema inicial ----------
        self.tema = obtener_tema()
        self.configure(bg=self.tema["fondo"])

        # ---------- Conexión a BD (Singleton) ----------
        self.bd = ConexionBD()
        self.bd.conectar()
        self.estado_bd = "Conectada" if self.bd.esta_conectado() else "Sin conexión"

        # ---------- Construir UI ----------
        self._construir_ui()

    # ------------------------------------------------------------
    def _construir_ui(self):
        tema = self.tema
        estado_bd = self.estado_bd

        # ==================== ENCABEZADO ====================
        self.header = tk.Frame(self, bg=tema["fondo_header"], height=80)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.lbl_logo = tk.Label(self.header, text="🏭 Autofactory",
                                 font=("Segoe UI", 22, "bold"),
                                 bg=tema["fondo_header"], fg="white")
        self.lbl_logo.pack(side="left", padx=25, pady=15)

        self.lbl_empresa = tk.Label(self.header, text=EMPRESA,
                                    font=("Segoe UI", 11),
                                    bg=tema["fondo_header"], fg="#B0BEC5")
        self.lbl_empresa.pack(side="left", pady=22)

        color_bd = "#2E7D32" if estado_bd == "Conectada" else "#C62828"
        self.lbl_bd = tk.Label(self.header, text=f"BD: {estado_bd}",
                               font=("Segoe UI", 10, "bold"),
                               bg=tema["fondo_header"], fg=color_bd)
        self.lbl_bd.pack(side="right", padx=10)

        self.lbl_usuario = tk.Label(self.header, text=f"Usuario: {AUTOR}",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=tema["fondo_header"], fg="#F9A825")
        self.lbl_usuario.pack(side="right", padx=10)

        # ---------- Botón de cambio de tema ----------
        self.btn_tema = tk.Button(
            self.header,
            text="🌙 Oscuro",
            command=self.cambiar_tema,
            font=("Segoe UI", 9, "bold"),
            bg="#F9A825", fg="#1B2A41",
            relief="flat", cursor="hand2",
            padx=12, pady=4
        )
        self.btn_tema.pack(side="right", padx=10)

        # ==================== NOTEBOOK (PESTAÑAS) ====================
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TNotebook",
                         background=tema["texto"],
                         borderwidth=0)
        estilo.configure("TNotebook.Tab",
                         font=("Segoe UI", 10, "bold"),
                         padding=[15, 8],
                         background=tema["tab_inactivo"],
                         foreground="white")
        estilo.map("TNotebook.Tab",
                   background=[("selected", tema["tab_activo"])],
                   foreground=[("selected", tema["texto"])])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # ==================== CARGA DE LOS 4 MÓDULOS ====================
        # Módulo 1: Vehículos (MVC) ✅
        self.vista_vehiculos = VistaVehiculos(self.notebook)
        self.notebook.add(self.vista_vehiculos, text="🚗 Vehículos")
        self.vista_vehiculos.controlador.cargar_datos()

        # Módulo 2: Producción (MVC) ✅
        self.vista_produccion = VistaProduccion(self.notebook)
        self.notebook.add(self.vista_produccion, text="🏗️ Producción")
        self.vista_produccion.controlador.cargar_datos()

        # Módulo 3: Inventario (MVC) ✅
        self.vista_inventario = VistaInventario(self.notebook)
        self.notebook.add(self.vista_inventario, text="📦 Inventario")
        self.vista_inventario.controlador.cargar_datos()

        # Módulo 4: Empleados (MVC) ✅
        self.vista_empleados = VistaEmpleados(self.notebook)
        self.notebook.add(self.vista_empleados, text="👷 Empleados")
        self.vista_empleados.controlador.cargar_datos()


        # ==================== BARRA DE ESTADO ====================
        self.status = tk.Label(
            self,
            text=f"Sistema listo  |  Base de datos: {'OK' if estado_bd == 'Conectada' else 'ERROR'}",
            anchor="w", bg=tema["fondo_status"], fg="white",
            font=("Segoe UI", 9), padx=15
        )
        self.status.pack(fill="x", side="bottom")

    # ------------------------------------------------------------
    def cambiar_tema(self):
        """Alterna entre tema claro y oscuro y refresca los colores."""
        alternar_tema()
        self.tema = obtener_tema()
        nombre = obtener_nombre_tema()

        tema = self.tema

        self.configure(bg=tema["fondo"])

        # Actualizar HEADER
        self.header.configure(bg=tema["fondo_header"])
        for widget in (self.lbl_logo, self.lbl_empresa,
                       self.lbl_bd, self.lbl_usuario):
            widget.configure(bg=tema["fondo_header"])

        # Actualizar STATUS
        self.status.configure(bg=tema["fondo_status"])

        # Actualizar el texto del botón
        if nombre == "oscuro":
            self.btn_tema.config(text="☀️ Claro")
        else:
            self.btn_tema.config(text="🌙 Oscuro")

        # Actualizar estilos del Notebook
        estilo = ttk.Style()
        estilo.configure("TNotebook", background=tema["texto"])
        estilo.configure("TNotebook.Tab",
                         background=tema["tab_inactivo"])
        estilo.map("TNotebook.Tab",
                   background=[("selected", tema["tab_activo"])],
                   foreground=[("selected", tema["texto"])])

        # Aplicar el tema a los 4 frames de los módulos
        for tab_id in self.notebook.tabs():
            frame = self.nametowidget(tab_id)
            aplicar_tema_ventana(frame, tema)

        # Actualizar la barra de estado
        self.status.config(
            text=f"Sistema listo  |  Tema: {nombre.upper()}  |  "
                 f"Base de datos: {'OK' if self.estado_bd == 'Conectada' else 'ERROR'}"
        )

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