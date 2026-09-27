"""Módulo de Producción - CRUD con Stored Procedures y tkcalendar."""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from config import FUENTE_TITULO, FUENTE_LABEL, PRIORIDADES, ESTADOS_ORDEN, TEMA_CLARO
from conexion_bd import ConexionBD
from utils.validaciones import crear_campo_fecha, solo_enteros
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf


class FrameProduccion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        self.bd = ConexionBD()
        self._construir()
        self.cargar_datos()

    def _construir(self):
        tk.Label(self, text="Módulo de Producción",
                 font=FUENTE_TITULO, bg=TEMA_CLARO["fondo"],
                 fg=TEMA_CLARO["texto"]).pack(pady=(20, 10))

        form = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        form.pack(pady=10)

        # -------- N° Orden (StringVar readonly) --------
        tk.Label(form, text="N° Orden:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=0, column=0, sticky="e", padx=5, pady=4)

        self.var_numero = tk.StringVar(value="")
        self.e_numero = tk.Entry(form, width=30,
                                 textvariable=self.var_numero,
                                 state="readonly",
                                 readonlybackground="#E0E0E0")
        self.e_numero.grid(row=0, column=1, padx=5, pady=4)

        # -------- Fecha emisión --------
        tk.Label(form, text="Fecha emisión:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=1, column=0, sticky="e", padx=5, pady=4)
        self.e_fecha = crear_campo_fecha(form)
        self.e_fecha.grid(row=1, column=1, padx=5, pady=4, sticky="w")

        # -------- Código modelo (solo enteros) --------
        tk.Label(form, text="Código modelo:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=2, column=0, sticky="e", padx=5, pady=4)
        vcmd = (self.register(solo_enteros), '%S')
        self.e_modelo = tk.Entry(form, width=30, validate="key", validatecommand=vcmd)
        self.e_modelo.grid(row=2, column=1, padx=5, pady=4)

        # -------- Cantidad (solo enteros) --------
        tk.Label(form, text="Cantidad:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=3, column=0, sticky="e", padx=5, pady=4)
        self.e_cantidad = tk.Entry(form, width=30, validate="key", validatecommand=vcmd)
        self.e_cantidad.grid(row=3, column=1, padx=5, pady=4)

        # -------- Fecha inicio --------
        tk.Label(form, text="Fecha inicio:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=4, column=0, sticky="e", padx=5, pady=4)
        self.e_finicio = crear_campo_fecha(form)
        self.e_finicio.grid(row=4, column=1, padx=5, pady=4, sticky="w")

        # -------- Fecha fin --------
        tk.Label(form, text="Fecha fin:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=5, column=0, sticky="e", padx=5, pady=4)
        self.e_ffin = crear_campo_fecha(form)
        self.e_ffin.grid(row=5, column=1, padx=5, pady=4, sticky="w")

        # -------- Prioridad --------
        tk.Label(form, text="Prioridad:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=6, column=0, sticky="e", padx=5, pady=4)
        self.c_prioridad = ttk.Combobox(form, values=PRIORIDADES,
                                        state="readonly", width=27)
        self.c_prioridad.current(1)
        self.c_prioridad.grid(row=6, column=1, padx=5, pady=4)

        # -------- Estado --------
        tk.Label(form, text="Estado:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=7, column=0, sticky="e", padx=5, pady=4)
        self.c_estado = ttk.Combobox(form, values=ESTADOS_ORDEN,
                                     state="readonly", width=27)
        self.c_estado.current(0)
        self.c_estado.grid(row=7, column=1, padx=5, pady=4)

        # -------- Botones --------
        botones = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        botones.pack(pady=15)

        # Botones CRUD
        for txt, cmd, color in [
            ("Guardar",    self.guardar,    TEMA_CLARO["primario"]),
            ("Actualizar", self.actualizar, "#1976D2"),
            ("Eliminar",   self.eliminar,   TEMA_CLARO["secundario"]),
            ("Limpiar",    self.limpiar,    "#757575"),
        ]:
            tk.Button(botones, text=txt, command=cmd,
                      bg=color, fg="white", width=12,
                      relief="flat", cursor="hand2"
                      ).pack(side="left", padx=5)

        # Botones de exportación (FUERA del bucle)
        tk.Button(botones, text="📊 Excel", command=self.exportar_excel,
                  bg="#1B5E20", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="📄 PDF", command=self.exportar_pdf,
                  bg="#B71C1C", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        # -------- Tabla --------
        cols = ("N° Orden", "Fecha", "Modelo", "Cantidad", "Prioridad", "Estado")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=140, anchor="center")
        self.tabla.pack(pady=15, padx=20, fill="x")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # ------------------------------------------------------------
    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        datos = self.bd.call_procedure("sp_listar_ordenes")
        if datos:
            for d in datos:
                self.tabla.insert("", "end", values=(
                    d["numero_produccion"], str(d["fecha_emision"]),
                    d["modelo"], d["cantidad_producir"],
                    d["prioridad"], d["estado_actual"]
                ))

    # ------------------------------------------------------------
    def guardar(self):
        try:
            self.bd.call_procedure("sp_insertar_orden", (
                self.e_fecha.get(),
                int(self.e_modelo.get() or 0),
                int(self.e_cantidad.get() or 0),
                self.e_finicio.get(),
                self.e_ffin.get(),
                self.c_prioridad.get(),
                self.c_estado.get()
            ))
            messagebox.showinfo("Éxito", "Orden registrada.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Verifique los valores numéricos.")

    # ------------------------------------------------------------
    def actualizar(self):
        numero = self.var_numero.get().strip()
        if not numero:
            messagebox.showwarning("Aviso", "Seleccione una orden de la tabla.")
            return
        if not messagebox.askyesno("Confirmar",
                                   f"¿Actualizar la orden {numero}?"):
            return
        try:
            self.bd.call_procedure("sp_actualizar_orden", (
                int(numero),
                self.e_fecha.get(),
                int(self.e_modelo.get() or 0),
                int(self.e_cantidad.get() or 0),
                self.e_finicio.get(),
                self.e_ffin.get(),
                self.c_prioridad.get(),
                self.c_estado.get()
            ))
            messagebox.showinfo("Éxito", "Orden actualizada.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")

    # ------------------------------------------------------------
    def eliminar(self):
        numero = self.var_numero.get().strip()
        if not numero:
            messagebox.showwarning("Aviso", "Seleccione una orden de la tabla.")
            return
        if not messagebox.askyesno("Confirmar",
            f"¿Eliminar la orden {numero}?\n\n"
            f"Esta acción no se puede deshacer."):
            return
        self.bd.call_procedure("sp_eliminar_orden", (int(numero),))
        messagebox.showinfo("Éxito", "Orden eliminada.")
        self.limpiar()
        self.cargar_datos()

    # ------------------------------------------------------------
    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]

        self.var_numero.set(str(v[0]))

        try:
            self.e_fecha.set_date(v[1])
        except Exception:
            pass

        self.e_modelo.delete(0, tk.END)
        self.e_modelo.insert(0, v[2])

        self.e_cantidad.delete(0, tk.END)
        self.e_cantidad.insert(0, v[3])

        self.c_prioridad.set(v[4])
        self.c_estado.set(v[5])

    # ------------------------------------------------------------
    def exportar_excel(self):
        datos = self.bd.call_procedure("sp_listar_ordenes")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("numero_produccion", "N° Orden"),
            ("fecha_emision", "Fecha"),
            ("modelo", "Modelo"),
            ("cantidad_producir", "Cantidad"),
            ("prioridad", "Prioridad"),
            ("estado_actual", "Estado"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Producción",
                         nombre_archivo="produccion")

    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.bd.call_procedure("sp_listar_ordenes")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("numero_produccion", "N° Orden"),
            ("fecha_emision", "Fecha"),
            ("modelo", "Modelo"),
            ("cantidad_producir", "Cantidad"),
            ("prioridad", "Prioridad"),
            ("estado_actual", "Estado"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Producción - AUTOfactory",
                       nombre_archivo="produccion")

    # ------------------------------------------------------------
    def limpiar(self):
        self.var_numero.set("")
        self.e_modelo.delete(0, tk.END)
        self.e_cantidad.delete(0, tk.END)

        hoy = datetime.date.today()
        self.e_fecha.set_date(hoy)
        self.e_finicio.set_date(hoy)
        self.e_ffin.set_date(hoy)

        self.c_prioridad.current(1)
        self.c_estado.current(0)