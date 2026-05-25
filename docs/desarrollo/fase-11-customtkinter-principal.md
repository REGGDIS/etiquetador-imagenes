# Fase 11 - CustomTkinter como interfaz principal

## Objetivo

Preparar CustomTkinter como interfaz principal de la aplicación, manteniendo la GUI Tkinter antigua disponible temporalmente como respaldo legacy durante la migración gradual.

## Archivos modificados o creados

- `main.py`: ahora abre la interfaz principal con CustomTkinter.
- `main_customtk.py`: queda como alias temporal para abrir la misma interfaz CustomTkinter.
- `main_tkinter_legacy.py`: nuevo punto de entrada temporal para abrir la GUI Tkinter antigua.
- `app/gui/customtk_window.py`: se quitaron textos de POC y prueba de concepto.
- `docs/desarrollo/fase-11-customtkinter-principal.md`: resumen técnico de la fase.

## Cambios realizados

- `python main.py` pasa a ejecutar `EtiquetadorCustomTkApp` desde `app/gui/customtk_window.py`.
- Se conserva `app/gui/main_window.py` sin cambios como implementación legacy.
- Se crea `main_tkinter_legacy.py` para ejecutar temporalmente la GUI antigua.
- `main_customtk.py` se mantiene como alias experimental/temporal hacia la misma interfaz CustomTkinter.
- La ventana CustomTkinter ya no muestra textos de POC ni de prueba de concepto.
- El título principal queda como `Etiquetador de Imágenes`.
- El subtítulo queda como `Organiza y etiqueta imágenes usando metadatos reales`.

## Decisiones técnicas

- Se mantiene una migración gradual: CustomTkinter queda como interfaz principal, pero Tkinter no se elimina todavía.
- No se modifican servicios de imágenes, metadatos ni normalización.
- No se modifica ExifTool ni su ruta de ejecución.
- No se agregan dependencias nuevas.
- No se modifica `requirements.txt` porque `customtkinter` ya está registrado.
- No se actualiza `README.md` en esta fase para mantener el cambio acotado.

## Cómo ejecutar la app principal

```powershell
.\venv\Scripts\python.exe main.py
```

También puede ejecutarse con:

```powershell
python main.py
```

## Cómo ejecutar temporalmente la GUI Tkinter legacy

```powershell
.\venv\Scripts\python.exe main_tkinter_legacy.py
```

También puede ejecutarse con:

```powershell
python main_tkinter_legacy.py
```

## Alias temporal CustomTkinter

`main_customtk.py` se conserva por ahora como alias temporal:

```powershell
.\venv\Scripts\python.exe main_customtk.py
```

## Verificaciones ejecutadas

- `.\venv\Scripts\python.exe -B -c "import main"`
- `.\venv\Scripts\python.exe -B -c "import main_customtk"`
- `.\venv\Scripts\python.exe -B -c "import main_tkinter_legacy"`
- `.\venv\Scripts\python.exe -B -c "import customtkinter; print('customtkinter OK')"`
- `git diff -- main.py main_customtk.py main_tkinter_legacy.py app/gui/customtk_window.py docs/desarrollo/fase-11-customtkinter-principal.md`
- `git diff --no-index -- /dev/null main_tkinter_legacy.py`
- `git status --short`

## Pruebas manuales recomendadas

1. Ejecutar `.\venv\Scripts\python.exe main.py`.
2. Confirmar que abre la interfaz CustomTkinter.
3. Abrir una carpeta con imágenes.
4. Confirmar que las imágenes se ven completas y grandes.
5. Navegar con Anterior y Siguiente.
6. Leer etiquetas existentes.
7. Guardar etiquetas nuevas.
8. Buscar una etiqueta existente.
9. Buscar una etiqueta inexistente.
10. Limpiar búsqueda.
11. Abrir otra carpeta después de limpiar.
12. Confirmar que no aparece error `pyimage`.
13. Confirmar que ExifTool sigue escribiendo `Keywords`.
14. Ejecutar `.\venv\Scripts\python.exe main_tkinter_legacy.py`.
15. Confirmar que la GUI Tkinter antigua sigue disponible como respaldo temporal.

## Estado final

- CustomTkinter queda como interfaz principal mediante `main.py`.
- Tkinter queda disponible temporalmente mediante `main_tkinter_legacy.py`.
- No se eliminaron archivos de GUI antigua.
- No se tocaron servicios.
- No se tocó ExifTool.
- No se agregaron dependencias.
- No se hizo commit.
