"""
Modelo de Vehículos - Acceso a datos.
Encapsula todas las llamadas a Stored Procedures relacionadas con
la tabla modelo_vehiculo.
"""
from conexion_bd import ConexionBD


class ModeloVehiculo:
    """Clase que gestiona el acceso a datos de vehículos."""

    def __init__(self):
        self.bd = ConexionBD()

    # ------------------------------------------------------------
    def listar(self):
        """Devuelve todos los modelos de vehículos."""
        return self.bd.call_procedure("sp_listar_modelos")

    # ------------------------------------------------------------
    def listar_por_categoria(self, categoria):
        """Devuelve modelos filtrados por categoría."""
        # Si no tenemos un SP específico, filtramos en Python
        todos = self.listar() or []
        return [m for m in todos if m["categoria"] == categoria]

    # ------------------------------------------------------------
    def insertar(self, nombre, categoria, especificaciones, tiempo_ensamble):
        """Inserta un nuevo modelo de vehículo."""
        return self.bd.call_procedure("sp_insertar_modelo", (
            nombre,
            categoria,
            especificaciones,
            int(tiempo_ensamble)
        ))

    # ------------------------------------------------------------
    def actualizar(self, codigo, nombre, categoria,
                   especificaciones, tiempo_ensamble):
        """Actualiza un modelo existente."""
        return self.bd.call_procedure("sp_actualizar_modelo", (
            int(codigo),
            nombre,
            categoria,
            especificaciones,
            int(tiempo_ensamble)
        ))

    # ------------------------------------------------------------
    def eliminar(self, codigo):
        """Elimina un modelo por su código."""
        return self.bd.call_procedure("sp_eliminar_modelo", (int(codigo),))

    # ------------------------------------------------------------
    def buscar(self, codigo):
        """Busca un modelo específico."""
        return self.bd.call_procedure("sp_buscar_modelo", (int(codigo),))