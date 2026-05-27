# Fase 13 - Archivar GUI Tkinter legacy

## Objetivo

Archivar la GUI Tkinter antigua en una carpeta `legacy` para dejar claro que CustomTkinter es la interfaz principal, sin eliminar todavía el respaldo temporal Tkinter.

## Archivos movidos

- `app/gui/main_window.py` se movio a `app/gui/legacy/tkinter_window.py`.

## Archivos modificados

- `main_tkinter_legacy.py`: actualiza el import de `EtiquetadorApp` para usar `app.gui.legacy.tkinter_window`.
- `README.md`: actualiza la estructura y el estado del proyecto para indicar que Tkinter esta archivado como legacy temporal.
- `docs/desarrollo/fase-13-archivar-gui-tkinter-legacy.md`: documenta esta fase.

## Archivos creados

- `app/gui/legacy/__init__.py`: marca la carpeta legacy como paquete Python.

## Estructura resultante

```text
app/gui/
├── __init__.py
├── customtk_window.py
└── legacy/
    ├── __init__.py
    └── tkinter_window.py
```

## Decisiones tecnicas

- CustomTkinter sigue siendo la interfaz principal mediante `main.py`.
- `main_customtk.py` se mantiene como alias temporal sin cambios.
- `main_tkinter_legacy.py` se mantiene como respaldo temporal para abrir la GUI Tkinter antigua.
- La clase `EtiquetadorApp` se conserva sin refactorizar en `app/gui/legacy/tkinter_window.py`.
- No se elimina la GUI Tkinter antigua para conservar un respaldo operativo durante la transicion.
- No se toca empaquetado `.exe` en esta fase.

## Que se mantuvo intacto

- `main.py`.
- `main_customtk.py`.
- `app/gui/customtk_window.py`.
- `app/services/image_service.py`.
- `app/services/metadata_service.py`.
- `app/services/tag_service.py`.
- `app/core/config.py`.
- `requirements.txt`.
- `.gitignore`.
- `exiftool.exe`.
- `exiftool_files/`.
- La lectura y escritura real de metadatos `Keywords` con ExifTool.
- La normalizacion de etiquetas.
- La busqueda interna por etiqueta exacta normalizada.

## Verificaciones ejecutadas

- `git status --short`: ejecutado al inicio; no mostro cambios pendientes.
- `.\venv\Scripts\python.exe -B -c "import main"`.
- `.\venv\Scripts\python.exe -B -c "import main_customtk"`.
- `.\venv\Scripts\python.exe -B -c "import main_tkinter_legacy"`.
- `git diff -- main_tkinter_legacy.py README.md docs/desarrollo/fase-13-archivar-gui-tkinter-legacy.md`.
- `git status --short`.
- Revision de existencia de `app/gui/main_window.py` y `app/gui/legacy/tkinter_window.py`.

## Pruebas manuales recomendadas

1. Ejecutar `.\venv\Scripts\python.exe main.py`.
2. Confirmar que abre CustomTkinter.
3. Abrir una carpeta con imagenes.
4. Navegar entre imagenes.
5. Verificar lectura y guardado de etiquetas.
6. Buscar una etiqueta existente.
7. Limpiar busqueda.
8. Ejecutar `.\venv\Scripts\python.exe main_tkinter_legacy.py`.
9. Confirmar que abre la GUI Tkinter legacy.
10. Confirmar que la GUI legacy puede abrir carpeta y navegar.

## Estado final

- La GUI principal sigue siendo CustomTkinter.
- La GUI Tkinter antigua queda archivada en `app/gui/legacy/tkinter_window.py`.
- `main_tkinter_legacy.py` sigue disponible como launcher temporal legacy.
- `app/gui/main_window.py` ya no queda en la raiz de `app/gui/`.
- No se modificaron servicios.
- No se modifico ExifTool.
- No se agregaron dependencias.
- No se hizo commit.
