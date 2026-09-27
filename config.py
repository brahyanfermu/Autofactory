"""
Configuración global de AUTOfactory.
Contiene credenciales de BD, colores, fuentes y constantes de negocio.
"""

# ============================================================
#  CONEXIÓN A LA BASE DE DATOS
# ============================================================
DB_HOST     = "localhost"
DB_PORT     = 3306
DB_USER     = "brahyan"           # <-- Cambia por tu usuario
DB_PASSWORD = "brahyan123"               # <-- Cambia por tu contraseña
DB_NAME     = "Autofactory"    # <-- Tu base de datos

# ============================================================
#  INFORMACIÓN DEL SISTEMA
# ============================================================
NOMBRE_APP = "AUTOfactory - Sistema de Gestión Automotriz"
VERSION    = "1.0.0"
EMPRESA    = "Motores Eficientes S.A."
AUTOR      = "Brahyan Fernández Múnera"

# ============================================================
#  TEMA CLARO (por defecto)
# ============================================================
TEMA_CLARO = {
    "fondo":         "#F5F7FA",
    "fondo_header":  "#1B2A41",
    "fondo_status":  "#C62828",
    "texto":         "#2C3E50",
    "texto_header":  "#FFFFFF",
    "primario":      "#2E7D32",
    "secundario":    "#C62828",
    "acento":        "#F9A825",
    "tab_inactivo":  "#34495E",
    "tab_activo":    "#F5F7FA",
}

# ============================================================
#  TEMA OSCURO
# ============================================================
TEMA_OSCURO = {
    "fondo":         "#1E1E1E",
    "fondo_header":  "#0D1117",
    "fondo_status":  "#C62828",
    "texto":         "#E8E8E8",
    "texto_header":  "#FFFFFF",
    "primario":      "#2E7D32",
    "secundario":    "#C62828",
    "acento":        "#F9A825",
    "tab_inactivo":  "#2D2D2D",
    "tab_activo":    "#1E1E1E",
}

# ============================================================
#  FUENTES
# ============================================================
FUENTE_TITULO = ("Segoe UI", 16, "bold")
FUENTE_LABEL  = ("Segoe UI", 10)
FUENTE_BOTON  = ("Segoe UI", 10, "bold")

# ============================================================
#  CONSTANTES DE NEGOCIO
# ============================================================
CATEGORIAS_VEHICULO = ["Sedan", "SUV", "Pickup"]
TURNOS              = ["Mañana", "Tarde", "Noche"]
PRIORIDADES         = ["Alta", "Media", "Baja"]
ESTADOS_ORDEN       = ["Pendiente", "En proceso", "Finalizada"]