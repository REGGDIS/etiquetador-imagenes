# 🖼️ Etiquetador de Imágenes

Aplicación de escritorio desarrollada en Python que permite visualizar imágenes desde una carpeta local y etiquetarlas fácilmente. Las etiquetas se guardan para facilitar su búsqueda posterior.

---

## 🚀 Funcionalidades actuales

- Visualización de imágenes desde una carpeta local.
- Navegación entre imágenes (anterior / siguiente).
- Campo de entrada para asignar etiquetas a cada imagen.
- Guardado automático de etiquetas en un archivo JSON.
- Interfaz gráfica sencilla con Tkinter.

---

## 🛠 Tecnologías utilizadas

- Python 3.12
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (GUI)
- [Pillow](https://python-pillow.org/) (para carga y manipulación de imágenes)
- JSON (almacenamiento de etiquetas)

---

## 💻 Cómo instalar y ejecutar

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/REGGDIS/etiquetador-imagenes.git
   cd etiquetador-imagenes
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado)**:

   ```bash
   python -m venv venv
   venv\Scripts\activate   # En Windows
   ```

3. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la app**:
   ```bash
   python main.py
   ```

---

## 🗂️ Estructura del proyecto

```
etiquetador-imagenes/
├── main.py               # Código principal de la aplicación
├── etiquetas.json        # Archivo donde se guardan las etiquetas (se genera automáticamente)
├── requirements.txt      # Dependencias necesarias
└── venv/                 # Entorno virtual (excluido del repositorio)
```

---

## 🔮 Próximas mejoras

- Migración de etiquetas a una base de datos SQLite.
- Búsqueda de imágenes por etiquetas.
- Exportación de etiquetas a Excel o CSV.
- Escritura de etiquetas en los metadatos del archivo (para ser reconocidas por el Explorador de Windows).
- Mejora del diseño de la interfaz con otros frameworks como PyQt o customTkinter.

---

## 🧑‍💻 Autor

Desarrollado por [REGGDIS](https://github.com/REGGDIS)  
¡Aprendiendo y creando soluciones útiles con Python!
