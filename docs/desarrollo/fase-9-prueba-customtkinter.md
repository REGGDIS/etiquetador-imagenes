# Fase 9 - Prueba de concepto con CustomTkinter

## Objetivo

Crear una interfaz experimental con CustomTkinter para evaluar una mejora visual sobre la GUI estable basada en Tkinter, sin reemplazar ni romper la ejecución actual con `python main.py`.

## Archivos creados o modificados

- `main_customtk.py`: nuevo punto de entrada experimental para la POC con CustomTkinter.
- `app/gui/customtk_window.py`: nueva ventana experimental implementada con CustomTkinter.
- `requirements.txt`: se agregó la dependencia `customtkinter`.
- `docs/desarrollo/fase-9-prueba-customtkinter.md`: resumen técnico de la fase.

## Qué se implementó

- Ventana experimental con `CTk`.
- Panel superior con título y acción principal para abrir carpeta.
- Panel informativo con nombre de imagen, contador y carpeta seleccionada.
- Panel central para previsualización de imagen.
- Panel de búsqueda por etiqueta exacta normalizada.
- Panel de edición y guardado de etiquetas.
- Navegación con botones Anterior y Siguiente.
- Estado inferior integrado en la zona de navegación.
- Aviso sobre etiquetas sin tildes ni caracteres especiales.
- Manejo básico de errores de carga de imagen y ExifTool.
- Estados básicos de botones según imágenes disponibles, navegación y búsqueda activa.

## Qué se mantuvo intacto

- `main.py`.
- `app/gui/main_window.py`.
- `app/services/image_service.py`.
- `app/services/metadata_service.py`.
- `app/services/tag_service.py`.
- `app/core/config.py`.
- `README.md`.
- `docs/instalacion-exiftool-windows.md`.
- `exiftool.exe` y `exiftool_files/`.

## Decisiones técnicas

- La POC queda aislada detrás de `main_customtk.py`.
- La GUI estable continúa ejecutándose con `python main.py`.
- La nueva ventana consume los servicios existentes para imágenes, metadatos y normalización.
- No se duplicó la lógica de ExifTool, carga de imágenes ni normalización.
- Se usó tema oscuro para evaluar una diferencia visual clara frente a Tkinter estándar.
- Se usó `CTkImage` para mostrar imágenes cargadas por Pillow.

## Dependencia agregada

- `customtkinter`.

No se agregaron otras dependencias.

## Cómo ejecutar la prueba

```powershell
python main_customtk.py
```

Con el entorno virtual del proyecto:

```powershell
.\venv\Scripts\python.exe main_customtk.py
```

La versión estable sigue ejecutándose con:

```powershell
python main.py
```

## Verificaciones ejecutadas

- `git status --short`
- `.\venv\Scripts\python.exe -B -c "import main"`
- `.\venv\Scripts\python.exe -B -c "import main_customtk"`
- `.\venv\Scripts\python.exe -B -c "import customtkinter; print('customtkinter OK')"`
- `git diff -- main_customtk.py app/gui/customtk_window.py requirements.txt docs/desarrollo/fase-9-prueba-customtkinter.md`
- `git status --short`

## Pruebas manuales recomendadas

1. Ejecutar `.\venv\Scripts\python.exe main_customtk.py`.
2. Confirmar que se abre la GUI CustomTkinter.
3. Abrir una carpeta con imágenes.
4. Confirmar que se muestran imágenes.
5. Navegar con Anterior y Siguiente.
6. Confirmar que el contador funciona.
7. Confirmar que lee etiquetas existentes.
8. Guardar etiquetas nuevas.
9. Verificar con ExifTool que se guardaron en `Keywords`.
10. Buscar una etiqueta existente.
11. Buscar una etiqueta inexistente.
12. Limpiar búsqueda.
13. Confirmar que `python main.py` sigue abriendo la GUI estable actual.
14. Comparar visualmente la versión Tkinter y CustomTkinter.
15. Indicar si CustomTkinter mejora lo suficiente como para justificar una migración completa.

## Riesgos o limitaciones detectadas

- La POC replica lógica de control de pantalla en una segunda clase GUI; si se aprueba la migración completa, conviene extraer lógica común de estado/búsqueda para reducir duplicación.
- La validación visual requiere pruebas manuales en Windows con imágenes reales.
- El empaquetado futuro como `.exe` deberá validar la inclusión correcta de CustomTkinter.
- La búsqueda sigue leyendo metadatos con ExifTool imagen por imagen, igual que la GUI estable.

## Estado final

- La POC CustomTkinter quedó aislada de la GUI estable.
- No se hizo commit.
