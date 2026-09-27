# 🏭 AUTOfactory

> **Sistema de Gestión para Industria Automotriz**
> Aplicación de escritorio desarrollada en Python con Tkinter para la empresa *Motores Eficientes S.A.*


---

## 📖 Descripción

**AUTOfactory** es una aplicación de escritorio modular desarrollada en **Python** con **Tkinter** que gestiona los principales procesos productivos de una fábrica de vehículos. El proyecto aplica **Programación Orientada a Objetos (POO)**, conexión a **MySQL** mediante **Stored Procedures**, y demuestra el manejo completo de interfaces gráficas de usuario con funcionalidades avanzadas.

La aplicación está organizada en **4 módulos funcionales** accesibles mediante un sistema de pestañas:

- 🚗 **Vehículos** — Registro de modelos con gestión de imágenes
- 🏗️ **Producción** — Órdenes con calendario flotante (tkcalendar)
- 📦 **Inventario** — Componentes con verificación de stock mínimo
- 👷 **Empleados** — Gestión de personal con imágenes y evaluación

---

## ✨ Características Principales

### 🔧 Funcionalidades Generales
- ✅ **CRUD completo** en los 4 módulos (Crear, Leer, Actualizar, Eliminar)
- ✅ **Conexión a MySQL** mediante Stored Procedures
- ✅ **Exportación a Excel** (openpyxl) y **PDF** (reportlab)
- ✅ **Tema claro/oscuro** intercambiable en tiempo real
- ✅ **Favicon personalizado** en la ventana
- ✅ **Interfaz moderna** con ttk.Notebook y estilos personalizados

### 📅 Validaciones Avanzadas
- ✅ **Calendario flotante** con tkcalendar para campos de fecha
- ✅ **Validación numérica estricta** (rechaza letras en tiempo real)
- ✅ **Validación de formatos** (JPG, PNG, GIF, tamaño máximo 5MB)
- ✅ **Confirmaciones** antes de operaciones críticas (eliminar/actualizar)

### 🖼️ Manejo de Imágenes
- ✅ **Carga de imágenes** con Pillow
- ✅ **Redimensionamiento automático** (150×150 px)
- ✅ **Vista previa** en Vehículos y Empleados
- ✅ **Copia automática** a carpeta del proyecto

---

## 🎯 Objetivos

### Objetivo General
Desarrollar una aplicación de escritorio funcional en Python que demuestre el manejo profesional de **interfaces gráficas con Tkinter**, **conexión a base de datos MySQL**, y **exportación de reportes**.

### Objetivos Específicos
- ✅ Aplicar POO mediante clases que heredan de `tk.Frame`
- ✅ Implementar CRUD con **Stored Procedures** en MySQL
- ✅ Usar **ttk.Notebook** para sistema de pestañas
- ✅ Implementar **tkcalendar** para selección de fechas
- ✅ Exportar datos a **Excel** (openpyxl) y **PDF** (reportlab)
- ✅ Gestionar **imágenes con Pillow** (redimensionar, validar)
- ✅ Implementar **tema claro/oscuro** intercambiable
- ✅ **Favicon personalizado** en la ventana

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| **Python** | 3.12 | Lenguaje principal |
| **Tkinter** | Estándar | Interfaz gráfica |
| **MySQL** | 8.0+ | Base de datos |
| **mysql-connector-python** | 9.1.0 | Conexión a MySQL |
| **openpyxl** | 3.1.5 | Exportar a Excel |
| **reportlab** | 5.0.1 | Exportar a PDF |
| **pillow** | 12.3.0 | Manejo de imágenes |
| **tkcalendar** | 1.6.1 | Calendario flotante |
| **PyCharm** | — | IDE de desarrollo |
| **DBeaver** | — | Cliente MySQL |
| **Git + GitHub** | — | Control de versiones |

---

## 📁 Estructura del Proyecto

```
6Autofactory/
│
├── main.py                       # Ventana principal + temas
├── config.py                     # Configuración global
├── conexion_bd.py                # Conexión MySQL (Singleton)
├── crear_icono.py                # Script para generar favicon
├── README.md
├── requirements.txt
├── .gitignore
│
├── modulos/                      # Los 4 módulos (pestañas)
│   ├── __init__.py
│   ├── mod_vehiculos.py
│   ├── mod_produccion.py
│   ├── mod_inventario.py
│   └── mod_empleados.py
│
├── utils/                        # Utilidades
│   ├── __init__.py
│   ├── validaciones.py           # Regex, tkcalendar
│   ├── exportar_excel.py         # openpyxl
│   ├── exportar_pdf.py           # reportlab
│   ├── imagenes.py               # Pillow
│   └── temas.py                  # Claro/Oscuro
│
├── sql/                          # Scripts BD
│   └── stored_procedures.sql     # 20 SP para CRUD
│
├── assets/                       # Recursos
│   ├── icono.ico
│   ├── icono.png
│   └── icono_grande.png
│
└── capturas/                     # Capturas e imágenes subidas
    └── imagenes/
```

---

## 🚀 Instalación y Ejecución

### Requisitos previos
- **Python 3.10+**
- **MySQL 8.0+** corriendo en `localhost:3306`
- **DBeaver** (opcional, para administrar la BD)

### 1. Clonar el repositorio
```bash
git clone https://github.com/brahyanfermu/6Autofactory.git
cd 6Autofactory
```

### 2. Crear y activar entorno virtual
```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

1. Abre **DBeaver** o **MySQL Workbench**
2. Ejecuta el script `sql/stored_procedures.sql` en tu BD `Autofactory`
3. Edita `config.py` con tus credenciales:

```python
DB_HOST     = "localhost"
DB_PORT     = 3306
DB_USER     = "root"
DB_PASSWORD = "tu_contraseña"
DB_NAME     = "Autofactory"
```

### 5. Ejecutar la aplicación
```bash
python main.py
```

---

## 🖥️ Uso de la Aplicación

### 🚗 Módulo de Vehículos
- Registra modelos de vehículos con código, nombre, categoría, especificaciones
- **Carga imágenes** con JPG/PNG/GIF (máx 5MB)
- Exporta a Excel y PDF

### 🏗️ Módulo de Producción
- Registra órdenes de producción con **calendario flotante** para las fechas
- Selecciona fechas con el calendario (no escribir)
- Botones: Guardar, Actualizar, Eliminar, Limpiar, Excel, PDF

### 📦 Módulo de Inventario
- Registra componentes con costo, stock mínimo, proveedor
- **Botón "Verificar Stock"**: muestra alerta si stock ≤ mínimo
- Validación numérica estricta

### 👷 Módulo de Empleados
- Registra empleados con foto (imagen)
- **Calendario flotante** para fecha de contratación
- Combobox para turno (Mañana/Tarde/Noche)

### 🌗 Cambio de Tema
- Botón **"🌙 Oscuro"** en el header
- Alterna entre tema claro y oscuro en tiempo real

---

## 🎓 Conceptos Técnicos Aplicados

### Principios de POO
- **Herencia** → Cada módulo hereda de `tk.Frame`
- **Encapsulamiento** → Widgets como atributos `self.widget`
- **Responsabilidad única** → Cada clase maneja un módulo

### Patrón Singleton
- **Conexión única** a MySQL durante toda la ejecución (`conexion_bd.py`)

### Stored Procedures
- **20 SP** creados en MySQL para las operaciones CRUD
- Uso desde Python con `cursor.callproc()`

### Validaciones
- **Regex** para números, DNI, RUC
- **tkcalendar** para fechas
- **messagebox** para feedback al usuario

---

## 📊 Base de Datos

- **Motor:** MySQL 8.0
- **Tablas:** 19 tablas relacionales
- **Vistas:** 5 vistas para reportes
- **Stored Procedures:** 20 SP (uno por operación CRUD)


---

## 👤 Autor

**Brahyan Fernández Múnera**
Estudiante de Desarrollo de Software
CEFIT — Envigado, Antioquia, Colombia

- 🐙 GitHub: [@brahyanfermu](https://github.com/brahyanfermu)
- 📧 Correo: brahyan1049@gmail.com

---

## 👨‍🏫 Docente

**James Mosquera Rentería**

CEFIT — Envigado, Antioquia

---

<div align="center">

**⭐ Si este proyecto te fue útil, dale una estrella en GitHub ⭐**



</div>