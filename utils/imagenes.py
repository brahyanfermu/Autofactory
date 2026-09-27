"""
Módulo para el manejo profesional de imágenes con Pillow.
Incluye: cargar, redimensionar, convertir formatos, validar tamaño.
"""
import os
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# ============================================================
#  CONFIGURACIÓN
# ============================================================
FORMATOS_PERMITIDOS = (".jpg", ".jpeg", ".png", ".gif")
TAMANO_MAXIMO_MB = 5
TAMANO_MAXIMO_BYTES = TAMANO_MAXIMO_MB * 1024 * 1024
TAMANO_VISTA_PREVIA = (150, 150)   # ancho x alto en píxeles

# Carpeta donde se guardan las imágenes subidas
CARPETA_IMAGENES = "capturas/imagenes"
os.makedirs(CARPETA_IMAGENES, exist_ok=True)


# ============================================================
#  VALIDACIONES
# ============================================================

def validar_archivo_imagen(ruta):
    """
    Valida que el archivo sea una imagen válida con formato y tamaño permitidos.
    Retorna (es_valido, mensaje_error).
    """
    if not ruta or not os.path.exists(ruta):
        return False, "El archivo no existe."

    # Validar formato
    ext = os.path.splitext(ruta)[1].lower()
    if ext not in FORMATOS_PERMITIDOS:
        return False, (
            f"Formato no permitido: {ext}\n\n"
            f"Formatos válidos: {', '.join(FORMATOS_PERMITIDOS)}"
        )

    # Validar tamaño
    tamano = os.path.getsize(ruta)
    if tamano > TAMANO_MAXIMO_BYTES:
        tamano_mb = tamano / (1024 * 1024)
        return False, (
            f"La imagen es muy grande: {tamano_mb:.2f} MB\n\n"
            f"Tamaño máximo permitido: {TAMANO_MAXIMO_MB} MB"
        )

    # Verificar que sea una imagen real (no solo la extensión)
    try:
        with Image.open(ruta) as img:
            img.verify()
        return True, ""
    except Exception:
        return False, "El archivo no es una imagen válida."


# ============================================================
#  CARGA Y PROCESAMIENTO
# ============================================================

def abrir_dialogo_imagen():
    """
    Abre un diálogo para seleccionar una imagen.
    Retorna la ruta seleccionada o None si el usuario cancela.
    """
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.jpg *.jpeg *.png *.gif"),
            ("JPG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("GIF", "*.gif"),
            ("Todos los archivos", "*.*"),
        ]
    )
    return ruta if ruta else None


def crear_miniatura(ruta, tamano=TAMANO_VISTA_PREVIA):
    """
    Carga una imagen, la redimensiona manteniendo la proporción
    y la convierte a formato Tkinter (PhotoImage).
    Retorna (photoimage, error).
    """
    try:
        img = Image.open(ruta)

        # Convertir a RGB si es necesario (GIF puede venir en modo P)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Redimensionar manteniendo la proporción
        img.thumbnail(tamano, Image.Resampling.LANCZOS)

        # Convertir a formato Tkinter
        foto = ImageTk.PhotoImage(img)
        return foto, None
    except Exception as e:
        return None, str(e)


def guardar_imagen_copiada(ruta_origen, prefijo):
    """
    Copia la imagen seleccionada a la carpeta del proyecto
    con un nombre único basado en el prefijo.
    Retorna la ruta final donde quedó guardada.
    """
    import datetime
    import shutil

    ext = os.path.splitext(ruta_origen)[1].lower()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"{prefijo}_{timestamp}{ext}"
    destino = os.path.join(CARPETA_IMAGENES, nombre)

    shutil.copy2(ruta_origen, destino)
    return destino


# ============================================================
#  FUNCIÓN DE ALTO NIVEL: SUBIR Y MOSTRAR
# ============================================================

def procesar_imagen_seleccionada(prefijo=""):
    """
    Abre el diálogo, valida la imagen, la copia al proyecto
    y devuelve (ruta_final, photoimage, error).

    Uso típico:
        ruta, foto, error = procesar_imagen_seleccionada("vehiculo")
        if error: mostrar error
        else: mostrar foto en un Label
    """
    ruta = abrir_dialogo_imagen()
    if not ruta:
        return None, None, None  # Usuario canceló

    # Validar
    valido, msg = validar_archivo_imagen(ruta)
    if not valido:
        return None, None, msg

    # Guardar copia en el proyecto
    try:
        ruta_final = guardar_imagen_copiada(ruta, prefijo)
    except Exception as e:
        return None, None, f"No se pudo copiar la imagen: {e}"

    # Crear miniatura
    foto, error = crear_miniatura(ruta_final)
    if error:
        return None, None, error

    return ruta_final, foto, None