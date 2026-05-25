# Fase 12 - Documentación de uso con CustomTkinter

## Objetivo

Actualizar la documentación de uso del proyecto para reflejar que CustomTkinter es la interfaz principal actual, manteniendo documentado el respaldo temporal con Tkinter legacy.

## Archivos modificados

- `README.md`: actualización de uso, tecnologías, ejecución, estructura y estado actual.
- `docs/desarrollo/fase-12-documentacion-customtkinter.md`: resumen técnico de la fase.

## Cambios realizados en README

- Se indicó que la interfaz principal actual usa CustomTkinter.
- Se mantuvo `python main.py` como comando principal de ejecución.
- Se agregó la ejecución directa con `.\venv\Scripts\python.exe main.py`.
- Se aclaró que `main_customtk.py` queda como alias temporal y no como entrada principal recomendada.
- Se documentó `main_tkinter_legacy.py` como respaldo temporal de la GUI Tkinter antigua.
- Se actualizó la sección de tecnologías para incluir CustomTkinter y Tkinter legacy.
- Se confirmó que `requirements.txt` incluye `pillow` y `customtkinter`.
- Se mantuvo la instrucción de ubicar `exiftool.exe` en la raíz del proyecto.
- Se documentó la búsqueda interna por etiqueta exacta normalizada.
- Se mantuvo la recomendación de escribir etiquetas sin tildes ni caracteres especiales.
- Se actualizó la estructura del proyecto para incluir `customtk_window.py`, `main_customtk.py`, `main_tkinter_legacy.py` y `tag_service.py`.

## Decisiones de documentación

- No se documentó PySide6 porque no forma parte del estado actual de la aplicación.
- No se documentó empaquetado `.exe` como funcionalidad implementada; queda solo como mejora futura.
- No se eliminó la guía de instalación de ExifTool.
- No se modificó el historial técnico de fases anteriores.
- No se agregaron capturas de pantalla.

## Estado actual de la interfaz principal

- `main.py` abre la interfaz principal con CustomTkinter.
- `app/gui/customtk_window.py` contiene la interfaz principal actual.
- `main_customtk.py` queda como alias temporal de CustomTkinter.
- `main_tkinter_legacy.py` permite abrir temporalmente la GUI Tkinter antigua.
- `app/gui/main_window.py` sigue existiendo como implementación legacy.

## Comandos principales de uso

Ejecutar la aplicación principal:

```powershell
python main.py
```

Ejecutar la aplicación principal con el entorno virtual:

```powershell
.\venv\Scripts\python.exe main.py
```

Ejecutar temporalmente la GUI Tkinter legacy:

```powershell
python main_tkinter_legacy.py
```

Verificar etiquetas guardadas con ExifTool:

```powershell
.\exiftool.exe -keywords -s3 "C:\ruta\a\imagen.jpg"
```

## Pruebas o verificaciones recomendadas

- Revisar que `README.md` indique CustomTkinter como interfaz principal.
- Ejecutar `python main.py` y confirmar que abre la interfaz CustomTkinter.
- Ejecutar `python main_tkinter_legacy.py` y confirmar que abre la GUI Tkinter antigua.
- Confirmar que las instrucciones de instalación siguen siendo válidas en Windows PowerShell.
- Confirmar que la guía de ExifTool sigue enlazada desde el README.
- Confirmar que la búsqueda por etiquetas y la normalización quedan descritas como funcionalidades actuales.

## Estado final

- Solo se modificó documentación.
- No se modificó código fuente.
- No se modificaron servicios.
- No se modificó `requirements.txt`.
- No se modificó ExifTool.
- No se crearon logs en `opencode-logs/`.
- No se hizo commit.
