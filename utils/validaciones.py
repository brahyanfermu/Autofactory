"""
Módulo de validaciones y utilidades para AUTOfactory.
Incluye:
- Validaciones con expresiones regulares (regex)
- Widget de fecha con calendario flotante (tkcalendar)
- Funciones auxiliares
"""
import re
import datetime
from tkinter import ttk
from tkcalendar import DateEntry


# ============================================================
#  VALIDACIONES CON REGEX
# ============================================================

def validar_solo_numeros(valor):
    """Verifica que el texto contenga solo dígitos."""
    if valor == "":
        return False
    return bool(re.fullmatch(r"\d+", str(valor)))


def validar_decimal(valor):
    """Verifica que sea un número decimal válido (positivo)."""
    if valor == "":
        return False
    return bool(re.fullmatch(r"\d+(\.\d{1,2})?", str(valor)))


def validar_email(email):
    """Valida formato de email con regex."""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.fullmatch(patron, email))


def validar_solo_letras(texto):
    """Verifica que solo contenga letras y espacios."""
    return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+", texto))


def validar_longitud(texto, minimo=1, maximo=255):
    """Valida que la longitud esté entre mínimo y máximo."""
    return minimo <= len(texto.strip()) <= maximo


def validar_dni(dni):
    """Valida DNI: solo dígitos, entre 5 y 20 caracteres."""
    return bool(re.fullmatch(r"\d{5,20}", str(dni)))


def validar_ruc(ruc):
    """Valida RUC: solo dígitos, entre 1 y 20 caracteres."""
    return bool(re.fullmatch(r"\d{1,20}", str(ruc)))


# ============================================================
#  WIDGET DE FECHA CON CALENDARIO FLOTANTE
# ============================================================

def crear_campo_fecha(parent, width=27):
    """
    Crea un widget DateEntry con calendario flotante en español.
    Uso:
        fecha = crear_campo_fecha(parent)
        fecha.get()          → devuelve string 'YYYY-MM-DD'
        fecha.get_date()     → devuelve objeto datetime.date
        fecha.set_date(d)    → establece una fecha
    """
    fecha = DateEntry(
        parent,
        width=width - 2,
        background="#2C3E50",
        foreground="white",
        borderwidth=2,
        date_pattern="yyyy-mm-dd",    # Formato ISO
        font=("Segoe UI", 9),
        locale="es_ES",                # Español
        showweeknumbers=False,
    )
    return fecha


# ============================================================
#  HELPERS AUXILIARES
# ============================================================

def hoy():
    """Devuelve la fecha de hoy como objeto date."""
    return datetime.date.today()


def fecha_a_texto(fecha):
    """Convierte un date/datetime a string 'YYYY-MM-DD'."""
    if isinstance(fecha, str):
        return fecha
    return fecha.strftime("%Y-%m-%d")


# ============================================================
#  VALIDADORES ESPECÍFICOS PARA AUTOFACTORY
# ============================================================

def validar_cantidad(valor):
    """Cantidad: entero positivo (para órdenes de producción)."""
    return validar_solo_numeros(valor) and int(valor) > 0


def validar_tiempo_ensamble(valor):
    """Tiempo de ensamble: entero positivo (horas)."""
    return validar_solo_numeros(valor) and int(valor) > 0


def validar_stock(valor):
    """Stock mínimo: entero no negativo."""
    return validar_solo_numeros(valor)


def validar_costo(valor):
    """Costo unitario: decimal positivo con hasta 2 decimales."""
    return validar_decimal(valor) and float(valor) > 0


def validar_evaluacion(valor):
    """Evaluación de desempeño: decimal entre 0.00 y 5.00."""
    if not validar_decimal(valor):
        return False
    v = float(valor)
    return 0.0 <= v <= 5.0