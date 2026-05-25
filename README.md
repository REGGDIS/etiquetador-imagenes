# Etiquetador de Imágenes

Aplicación de escritorio para Windows desarrollada en Python. Permite visualizar imágenes desde una carpeta local, navegar entre ellas y escribir etiquetas reales en los metadatos `Keywords` de cada archivo usando ExifTool.

El objetivo principal es facilitar que las imágenes puedan encontrarse posteriormente desde el Explorador de Windows mediante búsquedas por etiquetas.

La interfaz principal actual usa CustomTkinter. La antigua interfaz Tkinter se conserva temporalmente como respaldo legacy.

## Funcionalidades Actuales

- Selección de carpetas locales.
- Recorrido de imágenes dentro de carpetas y subcarpetas.
- Visualización de imágenes soportadas.
- Navegación con botones `Anterior` y `Siguiente`.
- Lectura de etiquetas existentes desde metadatos reales usando ExifTool.
- Escritura de múltiples etiquetas directamente en `Keywords`.
- Normalización básica de etiquetas antes de guardar.
- Búsqueda interna por etiqueta exacta normalizada.
- Limpieza de búsqueda para volver a la lista completa.
- Mensajes de estado dentro de la interfaz.
- Información de imagen actual, contador y carpeta seleccionada.
- Aviso visual de compatibilidad para escribir etiquetas sin tildes ni caracteres especiales.
- Búsqueda posterior desde el Explorador de Windows usando las etiquetas guardadas.

## Tecnologías Utilizadas

- Python 3.12
- CustomTkinter
- Tkinter como respaldo legacy temporal
- Pillow
- ExifTool
- Git/GitHub

## Requisitos Previos

- Windows como sistema principal de uso.
- Python instalado.
- ExifTool disponible en la raíz del proyecto como `exiftool.exe`.

Para configurar ExifTool en Windows, revisa `docs/instalacion-exiftool-windows.md`.

`exiftool.exe` y la carpeta `exiftool_files/` son archivos locales ignorados por Git mediante `.gitignore`, por lo que no se suben al repositorio.

## Instalación

Comandos para Windows PowerShell:

```powershell
git clone https://github.com/REGGDIS/etiquetador-imagenes.git
cd etiquetador-imagenes
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Después de instalar las dependencias, coloca `exiftool.exe` en la raíz del proyecto, junto a `main.py`.

El archivo `requirements.txt` incluye `pillow` y `customtkinter`.

## Ejecución

La interfaz principal actual usa CustomTkinter.

```powershell
python main.py
```

También puede ejecutarse directamente desde el entorno virtual:

```powershell
.\venv\Scripts\python.exe main.py
```

`main_customtk.py` queda disponible como alias temporal de la interfaz CustomTkinter, pero no es la ejecución principal recomendada.

### Interfaz Tkinter Legacy

La GUI Tkinter antigua se conserva temporalmente como respaldo:

```powershell
python main_tkinter_legacy.py
```

O con el entorno virtual:

```powershell
.\venv\Scripts\python.exe main_tkinter_legacy.py
```

## Uso Básico

1. Abrir la aplicación.
2. Presionar `Abrir carpeta`.
3. Seleccionar una carpeta que contenga imágenes.
4. Ver la imagen en el panel principal.
5. Navegar entre imágenes con `Anterior` y `Siguiente`.
6. Escribir etiquetas separadas por coma en el campo de etiquetas.
7. Presionar `Guardar etiquetas`.
8. Buscar imágenes por etiqueta exacta normalizada desde el campo de búsqueda.
9. Presionar `Limpiar` para volver a la lista completa.
10. Verificar las etiquetas desde el Explorador de Windows o con ExifTool.

## Verificación con ExifTool

Para revisar las etiquetas guardadas en una imagen:

```powershell
.\exiftool.exe -keywords -s3 "C:\ruta\a\imagen.jpg"
```

## Recomendación sobre Etiquetas

Se recomienda escribir etiquetas sin tildes ni caracteres especiales para mejorar la compatibilidad con el Explorador de Windows.

Ejemplos:

- Usar `expedicion` en vez de `expedición`.
- Usar `guia` en vez de `guía`.

## Estructura del Proyecto

```text
main.py
main_customtk.py              # alias temporal de CustomTkinter
main_tkinter_legacy.py        # respaldo temporal Tkinter
app/
├── __init__.py
├── core/
│   ├── __init__.py
│   └── config.py
├── gui/
│   ├── __init__.py
│   ├── customtk_window.py
│   └── main_window.py        # GUI Tkinter legacy
└── services/
    ├── __init__.py
    ├── image_service.py
    ├── metadata_service.py
    └── tag_service.py
README.md
requirements.txt
.gitignore
exiftool.exe          # local, ignorado por Git
exiftool_files/       # local, ignorado por Git
venv/                 # local, ignorado por Git
```

## Estado Actual del Proyecto

- La aplicación es funcional.
- `main.py` es el punto de entrada principal y abre la interfaz CustomTkinter.
- `app/gui/customtk_window.py` contiene la interfaz principal actual.
- `main_customtk.py` queda como alias temporal de la interfaz CustomTkinter.
- `main_tkinter_legacy.py` permite ejecutar temporalmente la GUI Tkinter antigua.
- `app/gui/main_window.py` contiene la interfaz Tkinter legacy.
- `app/services/image_service.py` contiene búsqueda y carga de imágenes.
- `app/services/metadata_service.py` contiene lectura y escritura de metadatos con ExifTool.
- `app/services/tag_service.py` contiene normalización de etiquetas.
- `app/core/config.py` contiene constantes simples del proyecto.
- Las etiquetas se guardan en metadatos reales `Keywords`, no en JSON ni en base de datos.
- El proyecto usa CustomTkinter como interfaz principal y está orientado principalmente a Windows.

## Próximas Mejoras Posibles

- Historial de etiquetas frecuentes.
- Autocompletado de etiquetas.
- Mejoras visuales adicionales sobre CustomTkinter.
- Empaquetado como `.exe`.
- Configuración manual de la ruta de ExifTool.
- Exportación CSV.

## Autor

Desarrollado por [REGGDIS](https://github.com/REGGDIS).
