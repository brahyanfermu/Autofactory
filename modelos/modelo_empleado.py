"""
Modelo de Empleados - Acceso a datos.
Encapsula todas las llamadas a Stored Procedures relacionadas con
la tabla empleado.
"""
from conexion_bd import ConexionBD


class ModeloEmpleado:
    """Clase que gestiona el acceso a datos de empleados."""

    def __init__(self):
        self.bd = ConexionBD()

    # ------------------------------------------------------------
    def listar(self):
        """Devuelve todos los empleados."""
        return self.bd.call_procedure("sp_listar_empleados")

    # ------------------------------------------------------------
    def insertar(self, nombres, apellido, dni, puesto, especializacion,
                 numero_linea, turno, fecha_contratacion, evaluacion):
        """Inserta un nuevo empleado."""
        return self.bd.call_procedure("sp_insertar_empleado", (
            nombres,
            apellido,
            dni,
            puesto,
            especializacion,
            int(numero_linea),
            turno,
            fecha_contratacion,
            float(evaluacion)
        ))

    # ------------------------------------------------------------
    def actualizar(self, numero, nombres, apellido, dni, puesto,
                   especializacion, numero_linea, turno,
                   fecha_contratacion, evaluacion):
        """Actualiza un empleado existente."""
        return self.bd.call_procedure("sp_actualizar_empleado", (
            int(numero),
            nombres,
            apellido,
            dni,
            puesto,
            especializacion,
            int(numero_linea),
            turno,
            fecha_contratacion,
            float(evaluacion)
        ))

    # ------------------------------------------------------------
    def eliminar(self, numero):
        """Elimina un empleado por su número."""
        return self.bd.call_procedure("sp_eliminar_empleado", (int(numero),))

    # ------------------------------------------------------------
    def buscar(self, numero):
        """Busca un empleado específico."""
        return self.bd.call_procedure("sp_buscar_empleado", (int(numero),))