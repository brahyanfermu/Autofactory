# 🏭 AUTOfactory

> **Sistema de Gestión para Industria Automotriz**
> Aplicación de escritorio desarrollada en Python con Tkinter para la empresa *Motores Eficientes S.A.*

## 📖 Descripción

**AUTOfactory** es una aplicación de escritorio modular desarrollada en **Python** con **Tkinter**
que simula la gestión de los principales procesos productivos de una fábrica de vehículos. 
El proyecto aplica **Programación Orientada a Objetos (POO)** y demuestra el manejo completo de interfaces gráficas de usuario.

La aplicación está organizada en **4 módulos funcionales** accesibles mediante un sistema de pestañas:

- 🚗 **Vehículos** — Registro de modelos con campo de clave oculta
- 🏗️ **Producción** — Registro de órdenes de producción
- 📦 **Inventario** — Verificación de stock con alertas visuales
- 👷 **Empleados** — Gestión del personal de producción


## 🎯 Objetivos del Proyecto

### Objetivo General
Desarrollar una aplicación de escritorio funcional en Python que demuestre el manejo de **interfaces gráficas con Tkinter**, aplicando principios de **Programación Orientada a Objetos** y estructuración modular del código.

### Objetivos Específicos
- ✅ Aplicar POO creando cada módulo como una clase que hereda de `tk.Frame`
- ✅ Implementar un sistema de navegación por pestañas con `ttk.Notebook`
- ✅ Manejar eventos de usuario mediante el parámetro `command=` de los botones
- ✅ Demostrar los **4 métodos clave de `Entry`**: `get()`, `delete()`, `insert()` y `config(show="*")`
- ✅ Validar datos de entrada y proporcionar feedback visual con `messagebox`
- ✅ Mostrar listados de registros con el widget `ttk.Treeview`

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| **Python** | 3.10+ | Lenguaje principal |
| **Tkinter** | Estándar | Interfaz gráfica de usuario |
| **ttk** | Estándar | Widgets mejorados (Notebook, Combobox, Treeview) |
| **messagebox** | Estándar | Diálogos de feedback al usuario |
| **PyCharm** | — | IDE de desarrollo |
| **Git / GitHub** | — | Control de versiones |

> ⚠️ **Importante**: El proyecto **no requiere librerías externas**. Todo funciona con la librería estándar de Python.

---

## 📁 Estructura del Proyecto

```
Autofactory/
│
├── main.py              # Aplicación completa (módulos + ventana principal)
├── README.md            # Este archivo

```

---

## 🚀 Instalación

### Requisitos previos

- **Python 3.10 o superior** → [Descargar Python](https://www.python.org/downloads/)
- **Tkinter** (viene incluido en Python por defecto)
- **Git** (opcional, solo si vas a clonar)

### 1. Verificar que Python está instalado

```bash
python --version
```

Deberías ver algo como: `Python 3.12.x`

### 2. Verificar que Tkinter está disponible

**En Windows / macOS:**
```bash
python -c "import tkinter; print('Tkinter OK')"
```

### 3. Clonar el repositorio (o descargarlo)

**Opción A — Con Git:**
```bash
git clone https://github.com/[tu-usuario]/autofactory.git
cd autofactory
```
**Opción B — Descarga manual:**
- Ve al repositorio en GitHub
- Clic en el botón verde **"Code"** → **"Download ZIP"**
- Descomprime el archivo
- Abre una terminal en la carpeta descomprimida

## ▶️ Uso

### Ejecutar la aplicación

Desde la terminal, en la carpeta del proyecto:

```bash
python main.py
```

**Desde PyCharm:**
1. Abre el proyecto
2. Clic derecho sobre `main.py`
3. Selecciona **"Run 'main'"** (o presiona `Shift + F10`)

### Se abrirá la ventana principal con:

- **Encabezado** — Nombre del sistema, empresa y usuario
- **4 pestañas** — Vehículos, Producción, Inventario, Empleados
- **Barra de estado** — Mensaje "Sistema listo"

---

## 🧩 Guía de Uso por Módulo

### 🚗 Módulo de Vehículos

**Propósito:** Registrar modelos de vehículos con validación.

**Cómo usar:**
1. Ingresa el **código del modelo** (ej: `MOD-001`)
2. Ingresa el **nombre** (ej: `Sedan Compacto`)
3. Selecciona una **categoría** en el Combobox (Sedan / SUV / Pickup)
4. Opcionalmente ingresa una **clave de acceso** (se muestra con asteriscos)
5. Clic en **"Guardar"** → el registro aparece en la tabla inferior
6. Clic en **"Limpiar"** → todos los campos se vacían

**Métodos de Entry demostrados:**
- `entry.get()` → Leer contenido (botón Guardar)
- `entry.delete(0, tk.END)` → Borrar todo (botón Limpiar)

---

### 🏗️ Módulo de Producción

**Propósito:** Registrar órdenes de producción.

**Cómo usar:**
1. Ingresa el **N° de orden** (ej: `OP-001`)
2. Ingresa la **cantidad** (ej: `50`)
3. Clic en **"Registrar Orden"**
4. Si todo está correcto, aparece un mensaje de éxito y los campos se limpian

---

### 📦 Módulo de Inventario

**Propósito:** Verificar si un componente tiene stock suficiente.

**Cómo usar:**
1. Ingresa el **código del componente** (ej: `COMP-001`)
2. Ingresa la **cantidad disponible** (ej: `5`)
3. Ingresa el **stock mínimo requerido** (ej: `10`)
4. Clic en **"Verificar Stock"**
5. Resultado:
   - 🔴 **Alerta roja** si `cantidad ≤ stock mínimo`
   - 🟢 **Mensaje verde** si hay stock suficiente
   - ❌ **Error** si ingresas texto en lugar de números

---

### 👷 Módulo de Empleados

**Propósito:** Registrar empleados de producción.

**Cómo usar:**
1. Ingresa el **N° de empleado** (ej: `EMP-001`)
2. Ingresa los **nombres** y **apellidos**
3. Selecciona el **turno** en el Combobox (Mañana / Tarde / Noche)
4. Clic en **"Registrar Empleado"**
5. Se muestra un mensaje de confirmación

---

## 🎓 Conceptos Técnicos Demostrados

### Widgets utilizados

| Widget | Ubicación | Uso |
|---|---|---|
| `tk.Tk` | `AplicacionAutofactory` | Ventana principal |
| `tk.Frame` | Cada módulo | Contenedor base |
| `tk.Label` | Encabezado, formularios | Texto no editable |
| `tk.Entry` | Formularios | Entrada de texto |
| `tk.Button` | Todos los módulos | Disparar acciones |
| `ttk.Combobox` | Vehículos, Empleados | Selección cerrada |
| `ttk.Notebook` | Ventana principal | Sistema de pestañas |
| `ttk.Treeview` | Vehículos | Tabla de registros |
| `messagebox` | Todas las acciones | Feedback al usuario |

### Métodos de `Entry` demostrados

```python
# 1. LEER contenido de un campo
codigo = self.entry_codigo.get()

# 2. BORRAR todo el contenido
self.entry_codigo.delete(0, tk.END)

# 3. INSERTAR texto en la posición 0
self.entry_codigo.insert(0, "MOD-001")

# 4. OCULTAR el texto (contraseña)
self.entry_clave.config(show="*")

# 5. MOSTRAR el texto de nuevo
self.entry_clave.config(show="")
```

### Principios de POO aplicados

- **Herencia** → Todas las clases de módulos heredan de `tk.Frame`
- **Encapsulamiento** → Cada módulo guarda sus widgets como `self.widget`
- **Métodos propios** → `guardar()`, `limpiar()`, `verificar()`, `registrar()`
- **Constructor** → Cada clase inicializa su UI en `__init__`
- **Responsabilidad única** → Cada clase maneja un solo módulo

### Estilos personalizados

```python
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TNotebook.Tab",
                 font=("Segoe UI", 10, "bold"),
                 padding=[15, 8],
                 background="#34495E",
                 foreground="white")
```
---

## 🎯 Características

- ✅ Interfaz gráfica moderna con sistema de pestañas
- ✅ Encabezado con identidad del sistema y del usuario
- ✅ Formularios con validación de campos
- ✅ Mensajes de feedback al usuario (éxito, advertencia, error)
- ✅ Tabla de registros con `ttk.Treeview`
- ✅ Estilos personalizados con colores corporativos
- ✅ Barra de estado informativa
- ✅ Código organizado en clases (POO)

---

## 👤 Autor

BRAHYAN FERNANDEZ MUNERA

Estudiante de Desarrollo de Software

CEFIT — Envigado, Antioquia, Colombia

- 📧 Correo: brahyan1049@gmail.com
- 🐙 GitHub: https://github.com/brahyanfermu/Autofactory.git

---

## 👨‍🏫 Docente

**James Mosquera Rentería**



