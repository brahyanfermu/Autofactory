"""
Módulo para exportar datos a PDF usando reportlab.
"""
import datetime
from tkinter import messagebox, filedialog

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer)


def exportar_a_pdf(datos, columnas, titulo, nombre_archivo):
    """
    Exporta una lista de diccionarios a un PDF con formato profesional.

    Parámetros:
        datos: lista de diccionarios
        columnas: lista de tuplas (clave, título_mostrar)
        titulo: título del reporte (ej: "Reporte de Vehículos")
        nombre_archivo: nombre sugerido (sin extensión)
    """
    if not datos:
        messagebox.showwarning("Sin datos", "No hay datos para exportar.")
        return

    # Preguntar dónde guardar
    ruta = filedialog.asksaveasfilename(
        title="Guardar como PDF",
        defaultextension=".pdf",
        initialfile=f"{nombre_archivo}_{datetime.date.today()}.pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not ruta:
        return

    try:
        doc = SimpleDocTemplate(
            ruta,
            pagesize=landscape(letter),
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
        )

        elementos = []
        estilos = getSampleStyleSheet()

        # ---------- Título ----------
        estilo_titulo = ParagraphStyle(
            "Titulo",
            parent=estilos["Title"],
            fontSize=18,
            textColor=colors.HexColor("#1B2A41"),
            spaceAfter=10,
        )
        elementos.append(Paragraph(titulo, estilo_titulo))

        # ---------- Subtítulo (fecha) ----------
        estilo_sub = ParagraphStyle(
            "Subtitulo",
            parent=estilos["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#757575"),
            spaceAfter=15,
        )
        fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        elementos.append(Paragraph(f"Generado el {fecha}", estilo_sub))
        elementos.append(Spacer(1, 10))

        # ---------- Tabla ----------
        encabezados = [h for _, h in columnas]
        filas = [encabezados]

        for item in datos:
            fila = [str(item.get(clave, "")) for clave, _ in columnas]
            filas.append(fila)

        tabla = Table(filas, repeatRows=1)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1B2A41")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0BEC5")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F5F7FA")]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabla)

        # ---------- Pie de página ----------
        elementos.append(Spacer(1, 20))
        estilo_pie = ParagraphStyle(
            "Pie",
            parent=estilos["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#757575"),
        )
        elementos.append(Paragraph(
            f"AUTOfactory - Motores Eficientes S.A.  |  "
            f"Total de registros: {len(datos)}",
            estilo_pie
        ))

        doc.build(elementos)
        messagebox.showinfo("Éxito",
            f"PDF generado correctamente:\n\n{ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n\n{e}")