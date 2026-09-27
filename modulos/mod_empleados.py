"""Módulo de Empleados - CRUD con Stored Procedures."""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from config import FUENTE_TITULO, FUENTE_LABEL, TURNOS, TEMA_CLARO
from conexion_bd import ConexionBD
from utils.validaciones import crear_campo_fecha


class FrameEmpleados(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        self.bd = ConexionBD()
        self._construir()
        self.cargar_datos()

    # ------------------------------------------------------------
    def _construir(self):
        tk.Label(self, text="Módulo de Empleados",
                 font=FUENTE_TITULO, bg=TEMA_CLARO["fondo"],
                 fg=TEMA_CLARO["texto"]).pack(pady=(20, 10))

        form = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        form.pack(pady=10)

        # Helper para crear campos rápidamente
        def campo(texto, fila, attr):
            tk.Label(form, text=texto, font=FUENTE_LABEL,
                     bg=TEMA_CLARO["fondo"]).grid(
                row=fila, column=0, sticky="e", padx=5, pady=4)
            entry = tk.Entry(form, width=30)
            entry.grid(row=fila, column=1, padx=5, pady=4)
            setattr(self, attr, entry)

        # ---------- N° Empleado (StringVar, readonly visual) ----------
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
        campo("DNI:", 3, "e_dni")
        campo("Puesto:", 4, "e_puesto")
        campo("Especialización:", 5, "e_especializacion")
        campo("N° Línea:", 6, "e_linea")

        # -------- Fecha contratación (con CALENDARIO) --------
        tk.Label(form, text="Fecha contratación:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=7, column=0, sticky="e", padx=5, pady=4)
        self.e_fecha = crear_campo_fecha(form)
        self.e_fecha.grid(row=7, column=1, padx=5, pady=4, sticky="w")

        campo("Evaluación (0.00 - 5.00):", 8, "e_evaluacion")

        # ---------- Combobox Turno ----------
        tk.Label(form, text="Turno:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(
            row=9, column=0, sticky="e", padx=5, pady=4)
        self.c_turno = ttk.Combobox(form, values=TURNOS,
                                    state="readonly", width=27)
        self.c_turno.current(0)
        self.c_turno.grid(row=9, column=1, padx=5, pady=4)

        # ---------- Botones ----------
        botones = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        botones.pack(pady=15)

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

        # ---------- Tabla ----------
        cols = ("N°", "Nombres", "Apellido", "DNI", "Puesto",
                "Especialización", "Línea", "Turno", "Evaluación")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=7)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=110, anchor="center")
        self.tabla.pack(pady=15, padx=20, fill="x")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # ------------------------------------------------------------
    def cargar_datos(self):
        """Llama al SP sp_listar_empleados y llena la tabla."""
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
        """Llama a sp_insertar_empleado."""
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
        """Llama a sp_actualizar_empleado."""
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
        """Llama a sp_eliminar_empleado."""
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
        """Al hacer clic en una fila, llena el formulario."""
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]

        # N° empleado usando StringVar
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
    def limpiar(self):
        """Limpia todos los campos del formulario."""
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