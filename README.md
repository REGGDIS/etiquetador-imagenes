# 🖼️ Etiquetador de Imágenes con ExifTool

Aplicación de escritorio desarrollada en Python que permite visualizar imágenes desde una carpeta local y etiquetarlas fácilmente. Las etiquetas se guardan directamente en los metadatos de cada archivo utilizando [ExifTool](https://exiftool.org/), lo que permite realizar búsquedas desde el Explorador de Windows.

---

## 🚀 Funcionalidades actuales

- Visualización de imágenes desde una carpeta (y subcarpetas).
- Navegación entre imágenes (anterior / siguiente).
- Asignación de múltiples etiquetas a cada imagen.
- Guardado directo de etiquetas en los metadatos de los archivos (`Keywords`).
- Lectura automática de las etiquetas existentes al visualizar una imagen.
- Interfaz gráfica intuitiva con Tkinter.
- Búsqueda de imágenes posible desde el Explorador de Windows utilizando las etiquetas.

---

## 🛠 Tecnologías utilizadas

- Python 3.12
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (Interfaz gráfica)
- [Pillow](https://python-pillow.org/) (Carga y manipulación de imágenes)
- [ExifTool](https://exiftool.org/) (Lectura y escritura de metadatos)

---

## 💻 Cómo instalar y ejecutar

1. **Clona el repositorio**:

```bash
git clone https://github.com/REGGDIS/etiquetador-imagenes.git
cd etiquetador-imagenes
```

2. **Crea y activa un entorno virtual (opcional, recomendado)**:

```bash
python -m venv venv
venv\Scripts\activate   # En Windows
```

3. **Instala las dependencias**:

```bash
pip install -r requirements.txt
```

4. **Coloca `exiftool.exe` en la carpeta raíz del proyecto** (junto a `main.py`).  
   Puedes descargarlo desde [ExifTool Official Website](https://exiftool.org/).

5. **Ejecuta la app**:

```bash
python main.py
```

---

## 📂 Estructura del proyecto

```
etiquetador-imagenes/
├── main.py                 # Código principal de la aplicación
├── exiftool.exe            # Herramienta para manejar metadatos (no se sube a GitHub)
├── .gitignore              # Exclusión de archivos como exiftool.exe y venv
├── README.md                # Documentación del proyecto
└── requirements.txt        # Dependencias necesarias
```

---

## 🔮 Próximas mejoras

- Implementar búsqueda de imágenes por etiqueta desde la aplicación.
- Exportar listado de imágenes y etiquetas a CSV o Excel.
- Empaquetar la app como ejecutable `.exe` para distribuir sin requerir Python.
- Mejorar la visualización de imágenes (centrado y ajuste dinámico de tamaño).

---

## 👨‍💻 Autor

Desarrollado por [REGGDIS](https://github.com/REGGDIS)  
¡Aprendiendo y creando soluciones útiles con Python!
