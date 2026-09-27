"""Módulo de Empleados - CRUD con Stored Procedures, tkcalendar e imágenes."""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from config import FUENTE_TITULO, FUENTE_LABEL, TURNOS, TEMA_CLARO
from conexion_bd import ConexionBD
from utils.validaciones import crear_campo_fecha, solo_enteros, solo_decimales
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf
from utils.imagenes import procesar_imagen_seleccionada


class FrameEmpleados(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        self.bd = ConexionBD()
        self.ruta_imagen = None
        self.foto_actual = None
        self._construir()
        self.cargar_datos()

    # ------------------------------------------------------------
    def _construir(self):
        tk.Label(self, text="Módulo de Empleados",
                 font=FUENTE_TITULO, bg=TEMA_CLARO["fondo"],
                 fg=TEMA_CLARO["texto"]).pack(pady=(20, 10))

        # -------- Contenedor principal (2 columnas) --------
        contenedor = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        contenedor.pack(pady=5)

        # -------- Columna izquierda: formulario --------
        form = tk.Frame(contenedor, bg=TEMA_CLARO["fondo"])
        form.grid(row=0, column=0, padx=15, pady=0)

        # Helper para crear campos rápidamente
        def campo(texto, fila, attr, validador=None):
            tk.Label(form, text=texto, font=FUENTE_LABEL,
                     bg=TEMA_CLARO["fondo"]).grid(
                row=fila, column=0, sticky="e", padx=5, pady=4)
            if validador:
                vcmd = (self.register(validador), '%S')
                entry = tk.Entry(form, width=30, validate="key", validatecommand=vcmd)
            else:
                entry = tk.Entry(form, width=30)
            entry.grid(row=fila, column=1, padx=5, pady=4)
            setattr(self, attr, entry)

        # ---------- N° Empleado (StringVar readonly) ----------
        tk.Label(form, text="N° Empleado:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=0, column=0, sticky="e", padx=5, pady=4)

        self.var_numero = tk.StringVar(value="")
        self.e_numero = tk.Entry(form, width=30,
                                 textvariable=self.var_numero,
                                 state="readonly",
                                 readonlybackground="#E0E0E0")
        self.e_numero.grid(row=0, column=1, padx=5, pady=4)

        campo("Nombres:", 1, "e_nombres")
        campo("Apellido:", 2, "e_apellido")
        campo("DNI:", 3, "e_dni", solo_enteros)
        campo("Puesto:", 4, "e_puesto")
        campo("Especialización:", 5, "e_especializacion")
        campo("N° Línea:", 6, "e_linea", solo_enteros)

        # -------- Fecha contratación (con CALENDARIO) --------
        tk.Label(form, text="Fecha contratación:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=7, column=0, sticky="e", padx=5, pady=4)
        self.e_fecha = crear_campo_fecha(form)
        self.e_fecha.grid(row=7, column=1, padx=5, pady=4, sticky="w")

        campo("Evaluación (0.00 - 5.00):", 8, "e_evaluacion", solo_decimales)

        # ---------- Combobox Turno ----------
        tk.Label(form, text="Turno:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(
            row=9, column=0, sticky="e", padx=5, pady=4)
        self.c_turno = ttk.Combobox(form, values=TURNOS,
                                    state="readonly", width=27)
        self.c_turno.current(0)
        self.c_turno.grid(row=9, column=1, padx=5, pady=4)

        # -------- Columna derecha: imagen --------
        marco_img = tk.LabelFrame(contenedor, text="Foto del Empleado",
                                  font=FUENTE_LABEL,
                                  bg=TEMA_CLARO["fondo"],
                                  fg=TEMA_CLARO["texto"],
                                  padx=10, pady=10)
        marco_img.grid(row=0, column=1, padx=15, pady=0)
        # Contenedor con tamaño FIJO en píxeles
        self.marco_prev = tk.Frame(marco_img,
                                   width=140,
                                   height=140,
                                   bg="#E0E0E0",
                                   relief="sunken",
                                   bd=1)
        self.marco_prev.pack(pady=(0, 10))
        self.marco_prev.pack_propagate(False)

        # Label que contiene la imagen
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
        cols = ("N°", "Nombres", "Apellido", "DNI", "Puesto",
                "Especialización", "Línea", "Turno", "Evaluación")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=6)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=110, anchor="center")
        self.tabla.pack(pady=10, padx=20, fill="x")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # ------------------------------------------------------------
    def cargar_imagen(self):
        ruta, foto, error = procesar_imagen_seleccionada(prefijo="empleado")

        if error:
            messagebox.showerror("Error de imagen", error)
            return
        if ruta is None:
            return

        self.ruta_imagen = ruta
        self.foto_actual = foto
        self.lbl_imagen.config(image=foto, text="")
        self.lbl_nombre_img.config(text=f"📎 {ruta.split('/')[-1]}")

        messagebox.showinfo("Éxito", "Imagen cargada correctamente.")

    # ------------------------------------------------------------
    def quitar_imagen(self):
        self.ruta_imagen = None
        self.foto_actual = None
        self.lbl_imagen.config(image="", text="Sin imagen")
        self.lbl_nombre_img.config(text="")

    # ------------------------------------------------------------
    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        datos = self.bd.call_procedure("sp_listar_empleados")
        if datos:
            for d in datos:
                self.tabla.insert("", "end", values=(
                    d["numero_empleado"],
                    d["nombres"],
                    d["apellido"],
                    d["DNI"],
                    d["puesto"],
                    d["especializacion"],
                    d["numero_linea"],
                    d["turno"],
                    d["evaluacion_desempeno"]
                ))

    # ------------------------------------------------------------
    def guardar(self):
        if not self.e_nombres.get().strip() or not self.e_apellido.get().strip():
            messagebox.showwarning("Validación", "Nombres y apellido son obligatorios.")
            return
        if not self.e_dni.get().strip():
            messagebox.showwarning("Validación", "El DNI es obligatorio.")
            return

        try:
            evaluacion = float(self.e_evaluacion.get() or 0)
            if evaluacion < 0 or evaluacion > 5:
                messagebox.showerror("Error",
                    "La evaluación debe estar entre 0.00 y 5.00.")
                return
        except ValueError:
            messagebox.showerror("Error",
                "La evaluación debe ser un número decimal (ej: 4.50).")
            return

        try:
            self.bd.call_procedure("sp_insertar_empleado", (
                self.e_nombres.get().strip(),
                self.e_apellido.get().strip(),
                self.e_dni.get().strip(),
                self.e_puesto.get().strip(),
                self.e_especializacion.get().strip(),
                int(self.e_linea.get() or 0),
                self.c_turno.get(),
                self.e_fecha.get(),
                evaluacion
            ))
            messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error",
                "Verifique que N° línea sea numérico.")

    # ------------------------------------------------------------
    def actualizar(self):
        numero = self.var_numero.get().strip()
        if not numero:
            messagebox.showwarning("Aviso", "Seleccione un empleado de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
                                   f"¿Actualizar al empleado {numero}?"):
            return

        try:
            evaluacion = float(self.e_evaluacion.get() or 0)
            self.bd.call_procedure("sp_actualizar_empleado", (
                int(numero),
                self.e_nombres.get().strip(),
                self.e_apellido.get().strip(),
                self.e_dni.get().strip(),
                self.e_puesto.get().strip(),
                self.e_especializacion.get().strip(),
                int(self.e_linea.get() or 0),
                self.c_turno.get(),
                self.e_fecha.get(),
                evaluacion
            ))
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")

    # ------------------------------------------------------------
    def eliminar(self):
        numero = self.var_numero.get().strip()
        if not numero:
            messagebox.showwarning("Aviso", "Seleccione un empleado de la tabla.")
            return

        if not messagebox.askyesno("Confirmar",
            f"¿Eliminar al empleado {numero}?\n\n"
            f"Esta acción no se puede deshacer."):
            return

        self.bd.call_procedure("sp_eliminar_empleado", (int(numero),))
        messagebox.showinfo("Éxito", "Empleado eliminado.")
        self.limpiar()
        self.cargar_datos()

    # ------------------------------------------------------------
    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]

        self.var_numero.set(str(v[0]))

        self.e_nombres.delete(0, tk.END)
        self.e_nombres.insert(0, v[1])

        self.e_apellido.delete(0, tk.END)
        self.e_apellido.insert(0, v[2])

        self.e_dni.delete(0, tk.END)
        self.e_dni.insert(0, v[3])

        self.e_puesto.delete(0, tk.END)
        self.e_puesto.insert(0, v[4])

        self.e_especializacion.delete(0, tk.END)
        self.e_especializacion.insert(0, v[5])

        self.e_linea.delete(0, tk.END)
        self.e_linea.insert(0, v[6])

        self.c_turno.set(v[7])

        self.e_evaluacion.delete(0, tk.END)
        self.e_evaluacion.insert(0, v[8])

        self.e_fecha.set_date(datetime.date.today())

    # ------------------------------------------------------------
    def exportar_excel(self):
        datos = self.bd.call_procedure("sp_listar_empleados")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("numero_empleado", "N°"),
            ("nombres", "Nombres"),
            ("apellido", "Apellido"),
            ("DNI", "DNI"),
            ("puesto", "Puesto"),
            ("especializacion", "Especialización"),
            ("numero_linea", "Línea"),
            ("turno", "Turno"),
            ("evaluacion_desempeno", "Evaluación"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Empleados",
                         nombre_archivo="empleados")

    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.bd.call_procedure("sp_listar_empleados")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("numero_empleado", "N°"),
            ("nombres", "Nombres"),
            ("apellido", "Apellido"),
            ("DNI", "DNI"),
            ("puesto", "Puesto"),
            ("especializacion", "Especialización"),
            ("numero_linea", "Línea"),
            ("turno", "Turno"),
            ("evaluacion_desempeno", "Evaluación"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Empleados - AUTOfactory",
                       nombre_archivo="empleados")

    # ------------------------------------------------------------
    def limpiar(self):
        self.var_numero.set("")

        for entry in (self.e_nombres,
                      self.e_apellido,
                      self.e_dni,
                      self.e_puesto,
                      self.e_especializacion,
                      self.e_linea,
                      self.e_evaluacion):
            entry.delete(0, tk.END)

        self.e_fecha.set_date(datetime.date.today())
        self.c_turno.current(0)
        self.quitar_imagen()