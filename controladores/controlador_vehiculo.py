"""
Controlador de Vehículos - Lógica de negocio.
Une el Modelo (datos) con la Vista (UI).
"""
from tkinter import messagebox

from modelos.modelo_vehiculo import ModeloVehiculo
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf


class ControladorVehiculo:
    """Coordina la Vista y el Modelo para el módulo de Vehículos."""

    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloVehiculo()

    # ------------------------------------------------------------
    #  CARGA DE DATOS
    # ------------------------------------------------------------
    def cargar_datos(self):
        """Carga los datos del modelo y los pasa a la vista."""
        datos = self.modelo.listar()
        self.vista.mostrar_datos_en_tabla(datos)

    # ------------------------------------------------------------
    #  GUARDAR (INSERT)
    # ------------------------------------------------------------
    def guardar(self):
        datos = self.vista.obtener_datos_formulario()

        # Validaciones
        if not datos["nombre"] or not datos["tiempo"]:
            messagebox.showwarning("Validación",
                "Nombre y tiempo son obligatorios.")
            return

        if not datos["tiempo"].isdigit():
            messagebox.showerror("Error",
                "El tiempo debe ser numérico.")
            return

        try:
            self.modelo.insertar(
                datos["nombre"],
                datos["categoria"],
                datos["especificaciones"],
                int(datos["tiempo"])
            )
            messagebox.showinfo("Éxito", "Modelo registrado.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar:\n{e}")

    # ------------------------------------------------------------
    #  ACTUALIZAR (UPDATE)
    # ------------------------------------------------------------
    def actualizar(self):
        datos = self.vista.obtener_datos_formulario()

        if not datos["codigo"]:
            messagebox.showwarning("Aviso",
                "Seleccione una fila de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Actualizar el modelo {datos['codigo']}?"):
            return

        try:
            self.modelo.actualizar(
                datos["codigo"],
                datos["nombre"],
                datos["categoria"],
                datos["especificaciones"],
                int(datos["tiempo"] or 0)
            )
            messagebox.showinfo("Éxito", "Modelo actualizado.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

    # ------------------------------------------------------------
    #  ELIMINAR (DELETE)
    # ------------------------------------------------------------
    def eliminar(self):
        datos = self.vista.obtener_datos_formulario()

        if not datos["codigo"]:
            messagebox.showwarning("Aviso",
                "Seleccione una fila de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Eliminar el modelo {datos['codigo']}?\n\n"
            f"Esta acción no se puede deshacer."):
            return

        try:
            self.modelo.eliminar(datos["codigo"])
            messagebox.showinfo("Éxito", "Modelo eliminado.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    # ------------------------------------------------------------
    #  EXPORTAR A EXCEL
    # ------------------------------------------------------------
    def exportar_excel(self):
        datos = self.modelo.listar()
        if not datos:
            messagebox.showwarning("Sin datos",
                "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_modelo", "Código"),
            ("nombre", "Nombre"),
            ("categoria", "Categoría"),
            ("especificaciones_tecnicas", "Especificaciones"),
            ("tiempo_ensamble", "Tiempo (h)"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Vehículos",
                         nombre_archivo="vehiculos")

    # ------------------------------------------------------------
    #  EXPORTAR A PDF
    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.modelo.listar()
        if not datos:
            messagebox.showwarning("Sin datos",
                "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_modelo", "Código"),
            ("nombre", "Nombre"),
            ("categoria", "Categoría"),
            ("especificaciones_tecnicas", "Especificaciones"),
            ("tiempo_ensamble", "Tiempo (h)"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Vehículos - AUTOfactory",
                       nombre_archivo="vehiculos")