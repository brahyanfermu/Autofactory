"""
Módulo de conexión a la base de datos MySQL Autofactory.
Patrón Singleton: una sola conexión durante toda la ejecución.
"""
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


class ConexionBD:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.conexion = None
        return cls._instancia

    # ------------------------------------------------------------
    def conectar(self):
        """Abre la conexión a MySQL."""
        try:
            self.conexion = mysql.connector.connect(
                host=DB_HOST, port=DB_PORT,
                user=DB_USER, password=DB_PASSWORD,
                database=DB_NAME, charset="utf8mb4"
            )
            if self.conexion.is_connected():
                print(f"[BD] Conectado a MySQL - DB: {DB_NAME}")
                return self.conexion
        except Error as e:
            print(f"[BD] Error: {e}")
            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar a '{DB_NAME}'.\n\nDetalle: {e}"
            )
            return None

    # ------------------------------------------------------------
    def esta_conectado(self):
        return self.conexion is not None and self.conexion.is_connected()

    # ------------------------------------------------------------
    def call_procedure(self, nombre_sp, params=()):
        """
        Ejecuta un Stored Procedure.
        - Si el SP devuelve filas (SELECT), retorna los resultados.
        - Si no devuelve filas (INSERT/UPDATE/DELETE), hace commit.
        """
        if not self.esta_conectado():
            messagebox.showerror("BD", "No hay conexión activa.")
            return None
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.callproc(nombre_sp, params)

            resultados = None
            for result in cursor.stored_results():
                resultados = result.fetchall()

            if resultados is None:
                # Era INSERT/UPDATE/DELETE
                self.conexion.commit()
                return []

            return resultados

        except Error as e:
            self.conexion.rollback()
            messagebox.showerror("Error SP", f"{nombre_sp}\n\n{e}")
            return None

    # ------------------------------------------------------------
    def cerrar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("[BD] Conexión cerrada.")