"""
Script para convertir una imagen PNG a ICO con múltiples tamaños.
Ejecutar UNA sola vez para generar los archivos del favicon.
"""
from PIL import Image
import os


# ---------- Configuración ----------
RUTA_PNG_ORIGEN = "assets/auto_favicon.png"   # ← Imagen que descargaste
RUTA_ICO_DESTINO = "assets/icono.ico"          # ← Se generará
RUTA_PNG_DESTINO = "assets/icono.png"          # ← Se generará

# Tamaños que tendrá el .ico (Windows/macOS los eligen según necesidad)
TAMANOS_ICO = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


def main():
    # Verificar que existe el PNG origen
    if not os.path.exists(RUTA_PNG_ORIGEN):
        print(f"❌ No existe el archivo: {RUTA_PNG_ORIGEN}")
        print(f"Coloca tu PNG en esa ruta y vuelve a ejecutar.")
        return

    # Abrir la imagen
    print(f"📂 Abriendo: {RUTA_PNG_ORIGEN}")
    img = Image.open(RUTA_PNG_ORIGEN)
    print(f"   Modo: {img.mode} | Tamaño: {img.size}")

    # Convertir a RGBA (para soportar transparencia)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        print(f"   Convertida a RGBA")

    # ------------------------------------------------------------
    # 1) Generar icono.ico con múltiples tamaños
    # ------------------------------------------------------------
    img.save(RUTA_ICO_DESTINO, format="ICO", sizes=TAMANOS_ICO)
    print(f"✅ Creado: {RUTA_ICO_DESTINO} ({len(TAMANOS_ICO)} tamaños)")

    # ------------------------------------------------------------
    # 2) Generar icono.png (32×32) para macOS/Linux
    # ------------------------------------------------------------
    img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    img_32.save(RUTA_PNG_DESTINO, format="PNG")
    print(f"✅ Creado: {RUTA_PNG_DESTINO} (32×32)")

    # ------------------------------------------------------------
    # 3) Generar icono_grande.png (256×256) para macOS Dock
    # ------------------------------------------------------------
    img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
    img_256.save("assets/icono_grande.png", format="PNG")
    print(f"✅ Creado: assets/icono_grande.png (256×256)")

    print("\n🎉 ¡Favicon generado con éxito!")
    print("   Ahora puedes usar los archivos en el código.")


if __name__ == "__main__":
    main()