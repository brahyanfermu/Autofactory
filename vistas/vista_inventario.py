"""
Vista de Inventario - Interfaz gráfica (UI).
Contiene SOLO la construcción de widgets y la captura de datos.
La lógica de negocio está en el controlador.
"""
import tkinter as tk
from tkinter import ttk

from config import FUENTE_TITULO, FUENTE_LABEL, TEMA_CLARO
from utils.validaciones import solo_enteros, solo_decimales


class VistaInventario(tk.Frame):
    """Interfaz gráfica del módulo de Inventario."""

    def __init__(self, parent):
        super().__init__(parent, bg=TEMA_CLARO["fondo"])
        # Importar aquí para evitar circular imports
        from controladores.controlador_inventario import ControladorInventario
        self.controlador = ControladorInventario(self)
        self._construir()

    # ------------------------------------------------------------
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

        tk.Button(botones, text="Guardar", command=self.controlador.guardar,
                  bg=TEMA_CLARO["primario"], fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        tk.Button(botones, text="Actualizar", command=self.controlador.actualizar,
                  bg="#1976D2", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        tk.Button(botones, text="Eliminar", command=self.controlador.eliminar,
                  bg=TEMA_CLARO["secundario"], fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        tk.Button(botones, text="Verificar Stock", command=self.controlador.verificar_stock,
                  bg=TEMA_CLARO["acento"], fg="white",
                  width=14, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        tk.Button(botones, text="Limpiar", command=self.limpiar_formulario,
                  bg="#757575", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        tk.Button(botones, text="📊 Excel", command=self.controlador.exportar_excel,
                  bg="#1B5E20", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        tk.Button(botones, text="📄 PDF", command=self.controlador.exportar_pdf,
                  bg="#B71C1C", fg="white",
                  width=12, relief="flat", cursor="hand2"
                  ).pack(side="left", padx=4)

        # -------- Tabla --------
        cols = ("Código", "Descripción", "Categoría", "Costo", "Stock mín.", "Proveedor")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=130, anchor="center")
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

        self.var_codigo.set(str(v[0]))

        self.e_desc.delete(0, tk.END);   self.e_desc.insert(0, v[1])
        self.e_cat.delete(0, tk.END);    self.e_cat.insert(0, v[2])
        self.e_costo.delete(0, tk.END);  self.e_costo.insert(0, v[3])
        self.e_stock.delete(0, tk.END);  self.e_stock.insert(0, v[4])

    def obtener_datos_formulario(self):
        """Devuelve los datos del formulario como diccionario."""
        return {
            "codigo": self.var_codigo.get().strip(),
            "descripcion": self.e_desc.get().strip(),
            "categoria": self.e_cat.get().strip(),
            "especificaciones": self.e_espec.get().strip(),
            "codigo_proveedor": self.e_prov.get().strip(),
            "tiempo_entrega": self.e_tiempo.get().strip(),
            "costo_unitario": self.e_costo.get().strip(),
            "stock_minimo": self.e_stock.get().strip(),
        }

    def mostrar_datos_en_tabla(self, datos):
        """Llena la tabla con los datos que le pasa el controlador."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        if datos:
            for d in datos:
                self.tabla.insert("", "end", values=(
                    d["codigo_componente"],
                    d["descripcion"],
                    d["categoria"],
                    d["costo_unitario"],
                    d["stock_minimo"],
                    d.get("proveedor") or ""
                ))

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.var_codigo.set("")
        for e in (self.e_desc, self.e_cat, self.e_espec,
                  self.e_prov, self.e_tiempo, self.e_costo, self.e_stock):
            e.delete(0, tk.END)