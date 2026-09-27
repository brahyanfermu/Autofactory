"""Módulo de Inventario - CRUD con Stored Procedures."""
import tkinter as tk
from tkinter import ttk, messagebox

from config import FUENTE_TITULO, FUENTE_LABEL, TEMA_CLARO
from conexion_bd import ConexionBD
from utils.validaciones import solo_enteros, solo_decimales
from utils.exportar_excel import exportar_a_excel
from utils.exportar_pdf import exportar_a_pdf


class FrameInventario(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        self.bd = ConexionBD()
        self._construir()
        self.cargar_datos()

    def _construir(self):
        tk.Label(self, text="Módulo de Inventario",
                 font=FUENTE_TITULO, bg=TEMA_CLARO["fondo"],
                 fg=TEMA_CLARO["texto"]).pack(pady=(20, 10))

        form = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        form.pack(pady=10)

        # -------- Código (StringVar readonly) --------
        tk.Label(form, text="Código componente:", font=FUENTE_LABEL,
                 bg=TEMA_CLARO["fondo"]).grid(row=0, column=0, sticky="e", padx=5, pady=4)

        self.var_codigo = tk.StringVar(value="")
        self.e_codigo = tk.Entry(form, width=30,
                                 textvariable=self.var_codigo,
                                 state="readonly",
                                 readonlybackground="#E0E0E0")
        self.e_codigo.grid(row=0, column=1, padx=5, pady=4)

        # -------- Helper para el resto de campos --------
        def campo(texto, fila, attr, validador=None):
            tk.Label(form, text=texto, font=FUENTE_LABEL,
                     bg=TEMA_CLARO["fondo"]).grid(row=fila, column=0, sticky="e", padx=5, pady=4)
            if validador:
                vcmd = (self.register(validador), '%S')
                e = tk.Entry(form, width=30, validate="key", validatecommand=vcmd)
            else:
                e = tk.Entry(form, width=30)
            e.grid(row=fila, column=1, padx=5, pady=4)
            setattr(self, attr, e)

        campo("Descripción:", 1, "e_desc")
        campo("Categoría:", 2, "e_cat")
        campo("Especificaciones:", 3, "e_espec")
        campo("Código proveedor:", 4, "e_prov", solo_enteros)
        campo("Tiempo entrega (días):", 5, "e_tiempo", solo_enteros)
        campo("Costo unitario:", 6, "e_costo", solo_decimales)
        campo("Stock mínimo:", 7, "e_stock", solo_enteros)

        # -------- Botones --------
        botones = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        botones.pack(pady=15)

        # Botones CRUD (dentro del bucle)
        for txt, cmd, color in [
            ("Guardar",         self.guardar,    TEMA_CLARO["primario"]),
            ("Actualizar",      self.actualizar, "#1976D2"),
            ("Eliminar",        self.eliminar,   TEMA_CLARO["secundario"]),
            ("Verificar Stock", self.verificar,  TEMA_CLARO["acento"]),
            ("Limpiar",         self.limpiar,    "#757575"),
        ]:
            tk.Button(botones, text=txt, command=cmd,
                      bg=color, fg="white", width=14,
                      relief="flat", cursor="hand2"
                      ).pack(side="left", padx=4)

        # Botones de exportación (FUERA del bucle)
        tk.Button(botones, text="📊 Excel", command=self.exportar_excel,
                  bg="#1B5E20", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        tk.Button(botones, text="📄 PDF", command=self.exportar_pdf,
                  bg="#B71C1C", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        # -------- Tabla --------
        cols = ("Código", "Descripción", "Categoría", "Costo", "Stock mín.", "Proveedor")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=5)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=130, anchor="center")
        self.tabla.pack(pady=10, padx=20, fill="x")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        # -------- Label de alerta --------
        self.lbl_alerta = tk.Label(
            self,
            text="",
            font=("Segoe UI", 14, "bold"),
            bg=TEMA_CLARO["fondo"],
            fg="#2E7D32",
            height=2,
            anchor="center"
        )
        self.lbl_alerta.pack(pady=10, fill="x")

    # ------------------------------------------------------------
    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        datos = self.bd.call_procedure("sp_listar_componentes")
        if datos:
            for d in datos:
                self.tabla.insert("", "end", values=(
                    d["codigo_componente"], d["descripcion"], d["categoria"],
                    d["costo_unitario"], d["stock_minimo"],
                    d.get("proveedor") or ""
                ))

    # ------------------------------------------------------------
    def guardar(self):
        try:
            self.bd.call_procedure("sp_insertar_componente", (
                self.e_desc.get(), self.e_cat.get(), self.e_espec.get(),
                int(self.e_prov.get() or 0), int(self.e_tiempo.get() or 0),
                float(self.e_costo.get() or 0), int(self.e_stock.get() or 0)
            ))
            messagebox.showinfo("Éxito", "Componente registrado.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Verifique valores numéricos.")

    # ------------------------------------------------------------
    def actualizar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Seleccione un componente de la tabla.")
            return
        if not messagebox.askyesno("Confirmar",
                                   f"¿Actualizar el componente {codigo}?"):
            return
        try:
            self.bd.call_procedure("sp_actualizar_componente", (
                int(codigo),
                self.e_desc.get(), self.e_cat.get(),
                self.e_espec.get(), int(self.e_prov.get() or 0),
                int(self.e_tiempo.get() or 0), float(self.e_costo.get() or 0),
                int(self.e_stock.get() or 0)
            ))
            messagebox.showinfo("Éxito", "Componente actualizado.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")

    # ------------------------------------------------------------
    def eliminar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Seleccione un componente de la tabla.")
            return
        if not messagebox.askyesno("Confirmar",
                                   f"¿Eliminar el componente {codigo}?\n\n"
                                   f"Esta acción no se puede deshacer."):
            return
        self.bd.call_procedure("sp_eliminar_componente", (int(codigo),))
        messagebox.showinfo("Éxito", "Componente eliminado.")
        self.limpiar()
        self.cargar_datos()

    # ------------------------------------------------------------
    def verificar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso",
                                   "Seleccione un componente de la tabla primero.")
            return

        datos = self.bd.call_procedure("sp_verificar_stock", (int(codigo),))

        if datos:
            d = datos[0]
            stock_actual = int(d["stock_actual"])
            stock_minimo = int(d["stock_minimo"])

            if d["estado_stock"] == "BAJO":
                messagebox.showerror(
                    "⚠ ALERTA: Stock BAJO",
                    f"Componente: {d['descripcion']}\n\n"
                    f"Stock actual: {stock_actual}\n"
                    f"Stock mínimo: {stock_minimo}\n\n"
                    f"⚠ Se requiere reposición inmediata.")
            else:
                messagebox.showinfo(
                    "✔ Stock SUFICIENTE",
                    f"Componente: {d['descripcion']}\n\n"
                    f"Stock actual: {stock_actual}\n"
                    f"Stock mínimo: {stock_minimo}\n\n"
                    f"✔ No se requiere reposición.")

    # ------------------------------------------------------------
    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]

        # Código con StringVar
        self.var_codigo.set(str(v[0]))

        self.e_desc.delete(0, tk.END);   self.e_desc.insert(0, v[1])
        self.e_cat.delete(0, tk.END);    self.e_cat.insert(0, v[2])
        self.e_costo.delete(0, tk.END);  self.e_costo.insert(0, v[3])
        self.e_stock.delete(0, tk.END);  self.e_stock.insert(0, v[4])

        self.lbl_alerta.config(text="")

    # ------------------------------------------------------------
    def exportar_excel(self):
        datos = self.bd.call_procedure("sp_listar_componentes")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_componente", "Código"),
            ("descripcion", "Descripción"),
            ("categoria", "Categoría"),
            ("costo_unitario", "Costo"),
            ("stock_minimo", "Stock mínimo"),
            ("proveedor", "Proveedor"),
        ]

        exportar_a_excel(datos, columnas,
                         titulo="Inventario",
                         nombre_archivo="inventario")

    # ------------------------------------------------------------
    def exportar_pdf(self):
        datos = self.bd.call_procedure("sp_listar_componentes")
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        columnas = [
            ("codigo_componente", "Código"),
            ("descripcion", "Descripción"),
            ("categoria", "Categoría"),
            ("costo_unitario", "Costo"),
            ("stock_minimo", "Stock mínimo"),
            ("proveedor", "Proveedor"),
        ]

        exportar_a_pdf(datos, columnas,
                       titulo="Reporte de Inventario - AUTOfactory",
                       nombre_archivo="inventario")

    # ------------------------------------------------------------
    def limpiar(self):
        self.var_codigo.set("")
        for e in (self.e_desc, self.e_cat, self.e_espec,
                  self.e_prov, self.e_tiempo, self.e_costo, self.e_stock):
            e.delete(0, tk.END)
        self.lbl_alerta.config(text="")