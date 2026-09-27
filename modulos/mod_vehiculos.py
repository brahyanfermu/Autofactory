"""Módulo de Vehículos - CRUD con Stored Procedures e imágenes."""
import tkinter as tk
from tkinter import ttk, messagebox

from config import (FUENTE_TITULO, FUENTE_LABEL,
                    CATEGORIAS_VEHICULO, TEMA_CLARO)
from conexion_bd import ConexionBD
from utils.validaciones import solo_enteros
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf
from utils.imagenes import procesar_imagen_seleccionada


class FrameVehiculos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        self.bd = ConexionBD()
        self.ruta_imagen = None   # Ruta de la imagen cargada
        self.foto_actual = None   # Objeto PhotoImage (para mantener referencia)
        self._construir()
        self.cargar_datos()

    # ------------------------------------------------------------
    def _construir(self):
        tk.Label(self, text="Módulo de Vehículos",
                 font=FUENTE_TITULO, bg=TEMA_CLARO["fondo"],
                 fg=TEMA_CLARO["texto"]).pack(pady=(20, 10))

        # -------- Contenedor principal (2 columnas) --------
        contenedor = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        contenedor.pack(pady=5)

        # -------- Columna izquierda: formulario --------
        form = tk.Frame(contenedor, bg=TEMA_CLARO["fondo"])
        form.grid(row=0, column=0, padx=15, pady=0)

        # ---------- Código (StringVar readonly) ----------
        tk.Label(form, text="Código:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.var_codigo = tk.StringVar(value="")
        self.e_codigo = tk.Entry(form, width=30,
                                 textvariable=self.var_codigo,
                                 state="readonly",
                                 readonlybackground="#E0E0E0")
        self.e_codigo.grid(row=0, column=1, padx=5, pady=5)

        # ---------- Nombre ----------
        tk.Label(form, text="Nombre:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.e_nombre = tk.Entry(form, width=30)
        self.e_nombre.grid(row=1, column=1, padx=5, pady=5)

        # ---------- Categoría ----------
        tk.Label(form, text="Categoría:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.c_categoria = ttk.Combobox(form, width=27,
                                        values=CATEGORIAS_VEHICULO,
                                        state="readonly")
        self.c_categoria.current(0)
        self.c_categoria.grid(row=2, column=1, padx=5, pady=5)

        # ---------- Especificaciones ----------
        tk.Label(form, text="Especificaciones:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.e_espec = tk.Entry(form, width=30)
        self.e_espec.grid(row=3, column=1, padx=5, pady=5)

        # ---------- Tiempo ensamble ----------
        tk.Label(form, text="Tiempo ensamble (h):", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        vcmd = (self.register(solo_enteros), '%S')
        self.e_tiempo = tk.Entry(form, width=30, validate="key", validatecommand=vcmd)
        self.e_tiempo.grid(row=4, column=1, padx=5, pady=5)

        # -------- Columna derecha: imagen --------
        marco_img = tk.LabelFrame(contenedor, text="Foto del Vehículo",
                                  font=FUENTE_LABEL,
                                  bg=TEMA_CLARO["fondo"],
                                  fg=TEMA_CLARO["texto"],
                                  padx=10, pady=10)
        marco_img.grid(row=0, column=1, padx=15, pady=0)

        # Vista previa
        # Contenedor con tamaño FIJO en píxeles
        self.marco_prev = tk.Frame(marco_img,
                                   width=140,
                                   height=140,
                                   bg="#E0E0E0",
                                   relief="sunken",
                                   bd=1)
        self.marco_prev.pack(pady=(0, 10))
        self.marco_prev.pack_propagate(False)  # ← CRÍTICO: no se encoge ni expande

        # Label que contiene la imagen (dentro del Frame)
        self.lbl_imagen = tk.Label(self.marco_prev,
                                   text="Sin imagen",
                                   font=("Segoe UI", 10),
                                   bg="#E0E0E0",
                                   fg="#757575")
        self.lbl_imagen.pack(fill="both", expand=True)

        # Nombre del archivo
        self.lbl_nombre_img = tk.Label(marco_img,
                                       text="",
                                       font=("Segoe UI", 8),
                                       bg=TEMA_CLARO["fondo"],
                                       fg="#757575",
                                       wraplength=150)
        self.lbl_nombre_img.pack(pady=(0, 10))

        # Botones de imagen
        tk.Button(marco_img, text="📁 Cargar Imagen",
                  command=self.cargar_imagen,
                  bg="#1976D2", fg="white",
                  width=18, relief="flat", cursor="hand2"
                  ).pack(pady=3)

        tk.Button(marco_img, text="🗑️ Quitar",
                  command=self.quitar_imagen,
                  bg="#757575", fg="white",
                  width=18, relief="flat", cursor="hand2"
                  ).pack(pady=3)

        # -------- Botones CRUD --------
        botones = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        botones.pack(pady=10)

        tk.Button(botones, text="Guardar", command=self.guardar,
                  bg=TEMA_CLARO["primario"], fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="Actualizar", command=self.actualizar,
                  bg="#1976D2", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="Eliminar", command=self.eliminar,
                  bg=TEMA_CLARO["secundario"], fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="Limpiar", command=self.limpiar,
                  bg="#757575", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="📊 Excel", command=self.exportar_excel,
                  bg="#1B5E20", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="📄 PDF", command=self.exportar_pdf,
                  bg="#B71C1C", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        # -------- Tabla --------
        cols = ("Código", "Nombre", "Categoría", "Especificaciones", "Tiempo")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=140, anchor="center")
        self.tabla.pack(pady=10, padx=20, fill="x")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # ------------------------------------------------------------
    def cargar_imagen(self):
        """Abre diálogo, valida, copia y muestra la imagen."""
        ruta, foto, error = procesar_imagen_seleccionada(prefijo="vehiculo")

        if error:
            messagebox.showerror("Error de imagen", error)
            return
        if ruta is None:
            return  # Usuario canceló

        self.ruta_imagen = ruta
        self.foto_actual = foto  # ¡Importante! Mantener referencia

        self.lbl_imagen.config(image=foto, text="")
        self.lbl_nombre_img.config(text=f"📎 {ruta.split('/')[-1]}")

        messagebox.showinfo("Éxito", "Imagen cargada correctamente.")

    # ------------------------------------------------------------
    def quitar_imagen(self):
        """Limpia la imagen del formulario."""
        self.ruta_imagen = None
        self.foto_actual = None
        self.lbl_imagen.config(image="", text="Sin imagen")
        self.lbl_nombre_img.config(text="")
    # ------------------------------------------------------------
    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        datos = self.bd.call_procedure("sp_listar_modelos")
        if datos:
            for d in datos:
                self.tabla.insert("", "end", values=(
                    d["codigo_modelo"], d["nombre"], d["categoria"],
                    d.get("especificaciones_tecnicas", "") or "",
                    d["tiempo_ensamble"]
                ))

    # ------------------------------------------------------------
    def guardar(self):
        nombre = self.e_nombre.get().strip()
        categoria = self.c_categoria.get()
        espec = self.e_espec.get().strip()
        tiempo = self.e_tiempo.get().strip()

        if not nombre or not tiempo:
            messagebox.showwarning("Validación", "Nombre y tiempo son obligatorios.")
            return

        if not tiempo.isdigit():
            messagebox.showerror("Error", "El tiempo debe ser numérico.")
            return

        self.bd.call_procedure("sp_insertar_modelo",
                               (nombre, categoria, espec, int(tiempo)))
        messagebox.showinfo("Éxito", "Modelo registrado.")
        self.limpiar()
        self.cargar_datos()

    # ------------------------------------------------------------
    def actualizar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Seleccione una fila de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
                                   f"¿Actualizar el modelo {codigo}?"):
            return

        try:
            self.bd.call_procedure("sp_actualizar_modelo", (
                int(codigo),
                self.e_nombre.get().strip(),
                self.c_categoria.get(),
                self.e_espec.get().strip(),
                int(self.e_tiempo.get() or 0)
            ))
            messagebox.showinfo("Éxito", "Modelo actualizado.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Verifique los valores numéricos.")

    # ------------------------------------------------------------
    def eliminar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Seleccione una fila de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
                                   f"¿Eliminar el modelo {codigo}?\n\n"
                                   f"Esta acción no se puede deshacer."):
            return

        self.bd.call_procedure("sp_eliminar_modelo", (int(codigo),))
        messagebox.showinfo("Éxito", "Modelo eliminado.")
        self.limpiar()
        self.cargar_datos()

    # ------------------------------------------------------------
    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]

        self.var_codigo.set(str(v[0]))

        self.e_nombre.delete(0, tk.END)
        self.e_nombre.insert(0, v[1])

        self.c_categoria.set(v[2])

        self.e_espec.delete(0, tk.END)
        self.e_espec.insert(0, v[3])

        self.e_tiempo.delete(0, tk.END)
        self.e_tiempo.insert(0, v[4])

    # ------------------------------------------------------------
    def exportar_excel(self):
        datos = self.bd.call_procedure("sp_listar_modelos")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_modelo", "Código"),
            ("nombre", "Nombre"),
            ("categoria", "Categoría"),
            ("especificaciones_tecnicas", "Especificaciones"),
            ("tiempo_ensamble", "Tiempo (h)"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Vehículos",
                         nombre_archivo="vehiculos")

    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.bd.call_procedure("sp_listar_modelos")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_modelo", "Código"),
            ("nombre", "Nombre"),
            ("categoria", "Categoría"),
            ("especificaciones_tecnicas", "Especificaciones"),
            ("tiempo_ensamble", "Tiempo (h)"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Vehículos - AUTOfactory",
                       nombre_archivo="vehiculos")

    # ------------------------------------------------------------
    def limpiar(self):
        self.var_codigo.set("")
        self.e_nombre.delete(0, tk.END)
        self.e_espec.delete(0, tk.END)
        self.e_tiempo.delete(0, tk.END)
        self.c_categoria.current(0)
        self.quitar_imagen()