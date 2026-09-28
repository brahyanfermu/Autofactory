"""
Controlador de Inventario - Lógica de negocio.
Une el Modelo (datos) con la Vista (UI).
"""
from tkinter import messagebox

from modelos.modelo_inventario import ModeloInventario
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf


class ControladorInventario:
    """Coordina la Vista y el Modelo para el módulo de Inventario."""

    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloInventario()

    # ------------------------------------------------------------
    def cargar_datos(self):
        """Carga los datos del modelo y los pasa a la vista."""
        datos = self.modelo.listar()
        self.vista.mostrar_datos_en_tabla(datos)

    # ------------------------------------------------------------
    def guardar(self):
        datos = self.vista.obtener_datos_formulario()

        # Validaciones
        if not datos["descripcion"]:
            messagebox.showwarning("Validación",
                "La descripción es obligatoria.")
            return

        try:
            self.modelo.insertar(
                datos["descripcion"],
                datos["categoria"],
                datos["especificaciones"],
                datos["codigo_proveedor"] or 0,
                datos["tiempo_entrega"] or 0,
                datos["costo_unitario"] or 0,
                datos["stock_minimo"] or 0
            )
            messagebox.showinfo("Éxito", "Componente registrado.")
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

        if not datos["codigo"]:
            messagebox.showwarning("Aviso",
                "Seleccione un componente de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Actualizar el componente {datos['codigo']}?"):
            return

        try:
            self.modelo.actualizar(
                datos["codigo"],
                datos["descripcion"],
                datos["categoria"],
                datos["especificaciones"],
                datos["codigo_proveedor"] or 0,
                datos["tiempo_entrega"] or 0,
                datos["costo_unitario"] or 0,
                datos["stock_minimo"] or 0
            )
            messagebox.showinfo("Éxito", "Componente actualizado.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

    # ------------------------------------------------------------
    def eliminar(self):
        datos = self.vista.obtener_datos_formulario()

        if not datos["codigo"]:
            messagebox.showwarning("Aviso",
                "Seleccione un componente de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Eliminar el componente {datos['codigo']}?\n\n"
            f"Esta acción no se puede deshacer."):
            return

        try:
            self.modelo.eliminar(datos["codigo"])
            messagebox.showinfo("Éxito", "Componente eliminado.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    # ------------------------------------------------------------
    def verificar_stock(self):
        """Verifica el stock del componente seleccionado."""
        datos = self.vista.obtener_datos_formulario()

        if not datos["codigo"]:
            messagebox.showwarning("Aviso",
                "Seleccione un componente de la tabla primero.")
            return

        resultado = self.modelo.verificar_stock(datos["codigo"])

        if resultado is None:
            messagebox.showwarning("Sin resultado",
                "No se pudo obtener información del componente.")
            return

        stock_actual = int(resultado["stock_actual"])
        stock_minimo = int(resultado["stock_minimo"])

        if resultado["estado_stock"] == "BAJO":
            messagebox.showerror(
                "⚠ ALERTA: Stock BAJO",
                f"Componente: {resultado['descripcion']}\n\n"
                f"Stock actual: {stock_actual}\n"
                f"Stock mínimo: {stock_minimo}\n\n"
                f"⚠ Se requiere reposición inmediata.")
        else:
            messagebox.showinfo(
                "✔ Stock SUFICIENTE",
                f"Componente: {resultado['descripcion']}\n\n"
                f"Stock actual: {stock_actual}\n"
                f"Stock mínimo: {stock_minimo}\n\n"
                f"✔ No se requiere reposición.")

    # ------------------------------------------------------------
    def exportar_excel(self):
        datos = self.modelo.listar()
        if not datos:
            messagebox.showwarning("Sin datos",
                "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_componente", "Código"),
            ("descripcion", "Descripción"),
            ("categoria", "Categoría"),
            ("costo_unitario", "Costo"),
            ("stock_minimo", "Stock mínimo"),
            ("proveedor", "Proveedor"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Inventario",
                         nombre_archivo="inventario")

    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.modelo.listar()
        if not datos:
            messagebox.showwarning("Sin datos",
                "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_componente", "Código"),
            ("descripcion", "Descripción"),
            ("categoria", "Categoría"),
            ("costo_unitario", "Costo"),
            ("stock_minimo", "Stock mínimo"),
            ("proveedor", "Proveedor"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Inventario - AUTOfactory",
                       nombre_archivo="inventario")