"""Módulo de Vehículos - CRUD con Stored Procedures."""
import tkinter as tk
from tkinter import ttk, messagebox

from config import (FUENTE_TITULO, FUENTE_LABEL,
                    CATEGORIAS_VEHICULO, TEMA_CLARO)
from conexion_bd import ConexionBD


class FrameVehiculos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        self.bd = ConexionBD()
        self._construir()
        self.cargar_datos()

    # ------------------------------------------------------------
    def _construir(self):
        tk.Label(self, text="Módulo de Vehículos",
                 font=FUENTE_TITULO, bg=TEMA_CLARO["fondo"],
                 fg=TEMA_CLARO["texto"]).pack(pady=(20, 10))

        form = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        form.pack(pady=10)

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
        self.e_tiempo = tk.Entry(form, width=30)
        self.e_tiempo.grid(row=4, column=1, padx=5, pady=5)

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
        cols = ("Código", "Nombre", "Categoría", "Especificaciones", "Tiempo")
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

        # Código con StringVar
        self.var_codigo.set(str(v[0]))

        self.e_nombre.delete(0, tk.END)
        self.e_nombre.insert(0, v[1])

        self.c_categoria.set(v[2])

        self.e_espec.delete(0, tk.END)
        self.e_espec.insert(0, v[3])

        self.e_tiempo.delete(0, tk.END)
        self.e_tiempo.insert(0, v[4])

    # ------------------------------------------------------------
    def limpiar(self):
        self.var_codigo.set("")
        self.e_nombre.delete(0, tk.END)
        self.e_espec.delete(0, tk.END)
        self.e_tiempo.delete(0, tk.END)
        self.c_categoria.current(0)