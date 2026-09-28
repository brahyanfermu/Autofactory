"""
Modelo de Producción - Acceso a datos.
Encapsula todas las llamadas a Stored Procedures relacionadas con
la tabla orden_produccion.
"""
from conexion_bd import ConexionBD


class ModeloProduccion:
    """Clase que gestiona el acceso a datos de órdenes de producción."""

    def __init__(self):
        self.bd = ConexionBD()

    # ------------------------------------------------------------
    def listar(self):
        """Devuelve todas las órdenes de producción."""
        return self.bd.call_procedure("sp_listar_ordenes")

    # ------------------------------------------------------------
    def insertar(self, fecha_emision, codigo_modelo, cantidad,
                 fecha_inicio, fecha_fin, prioridad, estado):
        """Inserta una nueva orden de producción."""
        return self.bd.call_procedure("sp_insertar_orden", (
            fecha_emision,
            int(codigo_modelo),
            int(cantidad),
            fecha_inicio,
            fecha_fin,
            prioridad,
            estado
        ))

    # ------------------------------------------------------------
    def actualizar(self, numero, fecha_emision, codigo_modelo, cantidad,
                   fecha_inicio, fecha_fin, prioridad, estado):
        """Actualiza una orden existente."""
        return self.bd.call_procedure("sp_actualizar_orden", (
            int(numero),
            fecha_emision,
            int(codigo_modelo),
            int(cantidad),
            fecha_inicio,
            fecha_fin,
            prioridad,
            estado
        ))

    # ------------------------------------------------------------
    def eliminar(self, numero):
        """Elimina una orden por su número."""
        return self.bd.call_procedure("sp_eliminar_orden", (int(numero),))

    # ------------------------------------------------------------
    def buscar(self, numero):
        """Busca una orden específica."""
        return self.bd.call_procedure("sp_buscar_orden", (int(numero),))