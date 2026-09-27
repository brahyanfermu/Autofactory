"""
Módulo de gestión de temas claro/oscuro.
"""
import tkinter as tk
from tkinter import ttk


# ============================================================
#  DICCIONARIOS DE TEMAS
# ============================================================

TEMAS = {
    "claro": {
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
    },
    "oscuro": {
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
    },
}

# Tema activo actual (por defecto: claro)
_tema_actual = "claro"


def obtener_tema():
    """Devuelve el diccionario del tema activo."""
    return TEMAS[_tema_actual]


def obtener_nombre_tema():
    """Devuelve el nombre del tema actual: 'claro' u 'oscuro'."""
    return _tema_actual


def alternar_tema():
    """
    Cambia entre tema claro y oscuro.
    Devuelve el nuevo diccionario del tema activo.
    """
    global _tema_actual
    _tema_actual = "oscuro" if _tema_actual == "claro" else "claro"
    return TEMAS[_tema_actual]


def aplicar_tema_ventana(ventana, tema):
    """
    Aplica los colores del tema a la ventana principal y sus
    hijos directos (header, notebook, status).
    """
    # Ventana principal
    ventana.configure(bg=tema["fondo"])

    # Recorrer todos los widgets de nivel superior
    for widget in ventana.winfo_children():
        _aplicar_recursivo(widget, tema)


def _aplicar_recursivo(widget, tema):
    """
    Recorre recursivamente los widgets aplicando el tema
    a Frames, Labels y Buttons.
    """
    try:
        clase = widget.winfo_class()

        # Frames
        if clase in ("Frame", "Labelframe", "TFrame", "TLabelframe"):
            widget.configure(bg=tema["fondo"])
            for child in widget.winfo_children():
                _aplicar_recursivo(child, tema)

        # Labels
        elif clase in ("Label", "TLabel"):
            try:
                widget.configure(bg=tema["fondo"])
            except tk.TclError:
                pass

        # Frames del Notebook
        elif clase == "TNotebook":
            for child in widget.winfo_children():
                _aplicar_recursivo(child, tema)

    except Exception:
        # Silenciar errores de widgets que no aceptan bg (ej: Combobox)
        pass