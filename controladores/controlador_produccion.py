"""
Controlador de Producción - Lógica de negocio.
Une el Modelo (datos) con la Vista (UI).
"""
from tkinter import messagebox

from modelos.modelo_produccion import ModeloProduccion
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf


class ControladorProduccion:
    """Coordina la Vista y el Modelo para el módulo de Producción."""

    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloProduccion()

    # ------------------------------------------------------------
    def cargar_datos(self):
        """Carga los datos del modelo y los pasa a la vista."""
        datos = self.modelo.listar()
        self.vista.mostrar_datos_en_tabla(datos)

    # ------------------------------------------------------------
    def guardar(self):
        datos = self.vista.obtener_datos_formulario()

        # Validaciones
        if not datos["codigo_modelo"] or not datos["cantidad"]:
            messagebox.showwarning("Validación",
                "Código de modelo y cantidad son obligatorios.")
            return

        try:
            self.modelo.insertar(
                datos["fecha_emision"],
                datos["codigo_modelo"],
                datos["cantidad"],
                datos["fecha_inicio"],
                datos["fecha_fin"],
                datos["prioridad"],
                datos["estado"]
            )
            messagebox.showinfo("Éxito", "Orden registrada.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error",
                "Verifique los valores numéricos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar:\n{e}")

    # ------------------------------------------------------------
    def actualizar(self):
        datos = self.vista.obtener_datos_formulario()

        if not datos["numero"]:
            messagebox.showwarning("Aviso",
                "Seleccione una orden de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Actualizar la orden {datos['numero']}?"):
            return

        try:
            self.modelo.actualizar(
                datos["numero"],
                datos["fecha_emision"],
                datos["codigo_modelo"],
                datos["cantidad"],
                datos["fecha_inicio"],
                datos["fecha_fin"],
                datos["prioridad"],
                datos["estado"]
            )
            messagebox.showinfo("Éxito", "Orden actualizada.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

    # ------------------------------------------------------------
    def eliminar(self):
        datos = self.vista.obtener_datos_formulario()

        if not datos["numero"]:
            messagebox.showwarning("Aviso",
                "Seleccione una orden de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Eliminar la orden {datos['numero']}?\n\n"
            f"Esta acción no se puede deshacer."):
            return

        try:
            self.modelo.eliminar(datos["numero"])
            messagebox.showinfo("Éxito", "Orden eliminada.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    # ------------------------------------------------------------
    def exportar_excel(self):
        datos = self.modelo.listar()
        if not datos:
            messagebox.showwarning("Sin datos",
                "No hay datos para exportar.")
            return

        columnas = [
            ("numero_produccion", "N° Orden"),
            ("fecha_emision", "Fecha"),
            ("modelo", "Modelo"),
            ("cantidad_producir", "Cantidad"),
            ("prioridad", "Prioridad"),
            ("estado_actual", "Estado"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Producción",
                         nombre_archivo="produccion")

    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.modelo.listar()
        if not datos:
            messagebox.showwarning("Sin datos",
                "No hay datos para exportar.")
            return

        columnas = [
            ("numero_produccion", "N° Orden"),
            ("fecha_emision", "Fecha"),
            ("modelo", "Modelo"),
            ("cantidad_producir", "Cantidad"),
            ("prioridad", "Prioridad"),
            ("estado_actual", "Estado"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Producción - AUTOfactory",
                       nombre_archivo="produccion")