"""
Modelo de Inventario - Acceso a datos.
Encapsula todas las llamadas a Stored Procedures relacionadas con
la tabla componente e inventario.
"""
from conexion_bd import ConexionBD


class ModeloInventario:
    """Clase que gestiona el acceso a datos de componentes e inventario."""

    def __init__(self):
        self.bd = ConexionBD()

    # ------------------------------------------------------------
    def listar(self):
        """Devuelve todos los componentes."""
        return self.bd.call_procedure("sp_listar_componentes")

    # ------------------------------------------------------------
    def insertar(self, descripcion, categoria, especificaciones,
                 codigo_proveedor, tiempo_entrega,
                 costo_unitario, stock_minimo):
        """Inserta un nuevo componente."""
        return self.bd.call_procedure("sp_insertar_componente", (
            descripcion,
            categoria,
            especificaciones,
            int(codigo_proveedor),
            int(tiempo_entrega),
            float(costo_unitario),
            int(stock_minimo)
        ))

    # ------------------------------------------------------------
    def actualizar(self, codigo, descripcion, categoria, especificaciones,
                   codigo_proveedor, tiempo_entrega,
                   costo_unitario, stock_minimo):
        """Actualiza un componente existente."""
        return self.bd.call_procedure("sp_actualizar_componente", (
            int(codigo),
            descripcion,
            categoria,
            especificaciones,
            int(codigo_proveedor),
            int(tiempo_entrega),
            float(costo_unitario),
            int(stock_minimo)
        ))

    # ------------------------------------------------------------
    def eliminar(self, codigo):
        """Elimina un componente por su código."""
        return self.bd.call_procedure("sp_eliminar_componente", (int(codigo),))

    # ------------------------------------------------------------
    def verificar_stock(self, codigo):
        """
        Llama al SP sp_verificar_stock y devuelve el primer resultado.
        Devuelve un dict con:
            codigo_componente, descripcion, stock_minimo,
            stock_actual, estado_stock ('BAJO' o 'SUFICIENTE')
        """
        resultado = self.bd.call_procedure("sp_verificar_stock", (int(codigo),))
        if resultado:
            return resultado[0]
        return None