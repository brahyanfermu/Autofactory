"""
Controlador de Empleados - Lógica de negocio.
Une el Modelo (datos) con la Vista (UI).
"""
from tkinter import messagebox

from modelos.modelo_empleado import ModeloEmpleado
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf


class ControladorEmpleado:
    """Coordina la Vista y el Modelo para el módulo de Empleados."""

    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloEmpleado()

    # ------------------------------------------------------------
    def cargar_datos(self):
        """Carga los datos del modelo y los pasa a la vista."""
        datos = self.modelo.listar()
        self.vista.mostrar_datos_en_tabla(datos)

    # ------------------------------------------------------------
    def guardar(self):
        datos = self.vista.obtener_datos_formulario()

        # Validaciones
        if not datos["nombres"] or not datos["apellido"]:
            messagebox.showwarning("Validación",
                "Nombres y apellido son obligatorios.")
            return

        if not datos["dni"]:
            messagebox.showwarning("Validación",
                "El DNI es obligatorio.")
            return

        try:
            evaluacion = float(datos["evaluacion"] or 0)
            if evaluacion < 0 or evaluacion > 5:
                messagebox.showerror("Error",
                    "La evaluación debe estar entre 0.00 y 5.00.")
                return
        except ValueError:
            messagebox.showerror("Error",
                "La evaluación debe ser un número decimal (ej: 4.50).")
            return

        try:
            self.modelo.insertar(
                datos["nombres"],
                datos["apellido"],
                datos["dni"],
                datos["puesto"],
                datos["especializacion"],
                datos["linea"] or 0,
                datos["turno"],
                datos["fecha"],
                evaluacion
            )
            messagebox.showinfo("Éxito", "Empleado registrado.")
            self.vista.limpiar_formulario()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error",
                "Verifique que el N° de línea sea numérico.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar:\n{e}")

    # ------------------------------------------------------------
    def actualizar(self):
        datos = self.vista.obtener_datos_formulario()

        if not datos["numero"]:
            messagebox.showwarning("Aviso",
                "Seleccione un empleado de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Actualizar al empleado {datos['numero']}?"):
            return

        try:
            evaluacion = float(datos["evaluacion"] or 0)
            self.modelo.actualizar(
                datos["numero"],
                datos["nombres"],
                datos["apellido"],
                datos["dni"],
                datos["puesto"],
                datos["especializacion"],
                datos["linea"] or 0,
                datos["turno"],
                datos["fecha"],
                evaluacion
            )
            messagebox.showinfo("Éxito", "Empleado actualizado.")
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
                "Seleccione un empleado de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Eliminar al empleado {datos['numero']}?\n\n"
            f"Esta acción no se puede deshacer."):
            return

        try:
            self.modelo.eliminar(datos["numero"])
            messagebox.showinfo("Éxito", "Empleado eliminado.")
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
            ("numero_empleado", "N°"),
            ("nombres", "Nombres"),
            ("apellido", "Apellido"),
            ("DNI", "DNI"),
            ("puesto", "Puesto"),
            ("especializacion", "Especialización"),
            ("numero_linea", "Línea"),
            ("turno", "Turno"),
            ("evaluacion_desempeno", "Evaluación"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Empleados",
                         nombre_archivo="empleados")

    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.modelo.listar()
        if not datos:
            messagebox.showwarning("Sin datos",
                "No hay datos para exportar.")
            return

        columnas = [
            ("numero_empleado", "N°"),
            ("nombres", "Nombres"),
            ("apellido", "Apellido"),
            ("DNI", "DNI"),
            ("puesto", "Puesto"),
            ("especializacion", "Especialización"),
            ("numero_linea", "Línea"),
            ("turno", "Turno"),
            ("evaluacion_desempeno", "Evaluación"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Empleados - AUTOfactory",
                       nombre_archivo="empleados")