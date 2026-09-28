"""
Vista de Producción - Interfaz gráfica (UI).
Contiene SOLO la construcción de widgets y la captura de datos.
La lógica de negocio está en el controlador.
"""
import tkinter as tk
from tkinter import ttk
import datetime

from config import (FUENTE_TITULO, FUENTE_LABEL,
                    PRIORIDADES, ESTADOS_ORDEN, TEMA_CLARO)
from utils.validaciones import crear_campo_fecha, solo_enteros


class VistaProduccion(tk.Frame):
    """Interfaz gráfica del módulo de Producción."""

    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        # Importar aquí para evitar circular imports
        from controladores.controlador_produccion import ControladorProduccion
        self.controlador = ControladorProduccion(self)
        self._construir()

    # ------------------------------------------------------------
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

        # -------- Fecha emisión (CALENDARIO) --------
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

        # -------- Fecha inicio (CALENDARIO) --------
        tk.Label(form, text="Fecha inicio:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=4, column=0, sticky="e", padx=5, pady=4)
        self.e_finicio = crear_campo_fecha(form)
        self.e_finicio.grid(row=4, column=1, padx=5, pady=4, sticky="w")

        # -------- Fecha fin (CALENDARIO) --------
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

        tk.Button(botones, text="Guardar", command=self.controlador.guardar,
                  bg=TEMA_CLARO["primario"], fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="Actualizar", command=self.controlador.actualizar,
                  bg="#1976D2", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="Eliminar", command=self.controlador.eliminar,
                  bg=TEMA_CLARO["secundario"], fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="Limpiar", command=self.limpiar_formulario,
                  bg="#757575", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="📊 Excel", command=self.controlador.exportar_excel,
                  bg="#1B5E20", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        tk.Button(botones, text="📄 PDF", command=self.controlador.exportar_pdf,
                  bg="#B71C1C", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=5)

        # -------- Tabla --------
        cols = ("N° Orden", "Fecha", "Modelo", "Cantidad", "Prioridad", "Estado")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=140, anchor="center")
        self.tabla.pack(pady=15, padx=20, fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

    # ------------------------------------------------------------
    #  MÉTODOS DE LA VISTA (solo UI, no lógica de negocio)
    # ------------------------------------------------------------

    def _al_seleccionar_fila(self, event):
        """Cuando el usuario hace clic en una fila, llena el formulario."""
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]

        self.var_numero.set(str(v[0]))

        # Cargar fechas en los DateEntry
        try:
            self.e_fecha.set_date(v[1])
            self.e_finicio.set_date(v[1])   # Aproximación
            self.e_ffin.set_date(v[1])      # Aproximación
        except Exception:
            pass

        self.e_modelo.delete(0, tk.END)
        self.e_modelo.insert(0, v[2])

        self.e_cantidad.delete(0, tk.END)
        self.e_cantidad.insert(0, v[3])

        self.c_prioridad.set(v[4])
        self.c_estado.set(v[5])

    def obtener_datos_formulario(self):
        """Devuelve los datos del formulario como diccionario."""
        return {
            "numero": self.var_numero.get().strip(),
            "fecha_emision": self.e_fecha.get(),
            "codigo_modelo": self.e_modelo.get().strip(),
            "cantidad": self.e_cantidad.get().strip(),
            "fecha_inicio": self.e_finicio.get(),
            "fecha_fin": self.e_ffin.get(),
            "prioridad": self.c_prioridad.get(),
            "estado": self.c_estado.get(),
        }

    def mostrar_datos_en_tabla(self, datos):
        """Llena la tabla con los datos que le pasa el controlador."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        if datos:
            for d in datos:
                self.tabla.insert("", "end", values=(
                    d["numero_produccion"],
                    str(d["fecha_emision"]),
                    d["modelo"],
                    d["cantidad_producir"],
                    d["prioridad"],
                    d["estado_actual"]
                ))

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.var_numero.set("")
        self.e_modelo.delete(0, tk.END)
        self.e_cantidad.delete(0, tk.END)

        # Fechas a hoy
        hoy = datetime.date.today()
        self.e_fecha.set_date(hoy)
        self.e_finicio.set_date(hoy)
        self.e_ffin.set_date(hoy)

        self.c_prioridad.current(1)
        self.c_estado.current(0)