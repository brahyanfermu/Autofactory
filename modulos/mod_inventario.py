"""Módulo de Inventario - CRUD con Stored Procedures."""
import tkinter as tk
from tkinter import ttk, messagebox

from config import FUENTE_TITULO, FUENTE_LABEL, TEMA_CLARO
from conexion_bd import ConexionBD


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

        def campo(texto, fila, attr):
            tk.Label(form, text=texto, font=FUENTE_LABEL,
                     bg=TEMA_CLARO["fondo"]).grid(row=fila, column=0, sticky="e", padx=5, pady=5)
            e = tk.Entry(form, width=30)
            e.grid(row=fila, column=1, padx=5, pady=5)
            setattr(self, attr, e)

        campo("Código componente:", 0, "e_codigo")
        campo("Descripción:", 1, "e_desc")
        campo("Categoría:", 2, "e_cat")
        campo("Especificaciones:", 3, "e_espec")
        campo("Código proveedor:", 4, "e_prov")
        campo("Tiempo entrega (días):", 5, "e_tiempo")
        campo("Costo unitario:", 6, "e_costo")
        campo("Stock mínimo:", 7, "e_stock")

        botones = tk.Frame(self, bg=TEMA_CLARO["fondo"])
        botones.pack(pady=15)

        for txt, cmd, color in [
            ("Guardar",    self.guardar,    TEMA_CLARO["primario"]),
            ("Actualizar", self.actualizar, "#1976D2"),
            ("Eliminar",   self.eliminar,   TEMA_CLARO["secundario"]),
            ("Verificar Stock", self.verificar, TEMA_CLARO["acento"]),
            ("Limpiar",    self.limpiar,    "#757575"),
        ]:
            tk.Button(botones, text=txt, command=cmd,
                      bg=color, fg="white", width=14,
                      relief="flat", cursor="hand2"
                      ).pack(side="left", padx=4)

        cols = ("Código", "Descripción", "Categoría", "Costo", "Stock mín.", "Proveedor")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=7)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=130, anchor="center")
        self.tabla.pack(pady=10, padx=20, fill="x")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.lbl_alerta = tk.Label(self, text="", font=("Segoe UI", 11, "bold"),
                                   bg=TEMA_CLARO["fondo"])
        self.lbl_alerta.pack(pady=5)

    def cargar_datos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        datos = self.bd.call_procedure("sp_listar_componentes")
        if datos:
            for d in datos:
                self.tabla.insert("", "end", values=(
                    d["codigo_componente"], d["descripcion"], d["categoria"],
                    d["costo_unitario"], d["stock_minimo"],
                    d.get("proveedor", "")
                ))

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

    def actualizar(self):
        if not self.e_codigo.get():
            return
        if not messagebox.askyesno("Confirmar", "¿Actualizar componente?"):
            return
        try:
            self.bd.call_procedure("sp_actualizar_componente", (
                int(self.e_codigo.get()), self.e_desc.get(), self.e_cat.get(),
                self.e_espec.get(), int(self.e_prov.get() or 0),
                int(self.e_tiempo.get() or 0), float(self.e_costo.get() or 0),
                int(self.e_stock.get() or 0)
            ))
            messagebox.showinfo("Éxito", "Componente actualizado.")
            self.limpiar()
            self.cargar_datos()
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")

    def eliminar(self):
        if not self.e_codigo.get():
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar componente?"):
            return
        self.bd.call_procedure("sp_eliminar_componente", (int(self.e_codigo.get()),))
        messagebox.showinfo("Éxito", "Componente eliminado.")
        self.limpiar()
        self.cargar_datos()

    def verificar(self):
        codigo = self.e_codigo.get()
        if not codigo:
            messagebox.showwarning("Aviso", "Ingrese el código del componente.")
            return
        datos = self.bd.call_procedure("sp_verificar_stock", (int(codigo),))
        if datos:
            d = datos[0]
            if d["estado_stock"] == "BAJO":
                self.lbl_alerta.config(
                    text=f"⚠ ALERTA: Stock BAJO ({d['stock_actual']} ≤ {d['stock_minimo']})",
                    fg="#C62828")
            else:
                self.lbl_alerta.config(
                    text=f"✔ Stock SUFICIENTE ({d['stock_actual']})",
                    fg="#2E7D32")

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]
        self.e_codigo.delete(0, tk.END); self.e_codigo.insert(0, v[0])
        self.e_desc.delete(0, tk.END);   self.e_desc.insert(0, v[1])
        self.e_cat.delete(0, tk.END);    self.e_cat.insert(0, v[2])
        self.e_costo.delete(0, tk.END);  self.e_costo.insert(0, v[3])
        self.e_stock.delete(0, tk.END);  self.e_stock.insert(0, v[4])

    def limpiar(self):
        for e in (self.e_codigo, self.e_desc, self.e_cat, self.e_espec,
                  self.e_prov, self.e_tiempo, self.e_costo, self.e_stock):
            e.delete(0, tk.END)
        self.lbl_alerta.config(text="")