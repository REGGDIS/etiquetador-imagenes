# Fase 18 - Mediciones temporales de rendimiento

## Objetivo

Agregar mediciones temporales de rendimiento para diagnosticar con datos donde estan los cuellos de botella de la aplicacion, tanto en desarrollo como en el build `.exe` generado con PyInstaller `onedir`.

## Problema detectado

La aplicacion funciona correctamente, pero la version empaquetada se siente lenta al abrir carpetas, navegar entre imagenes, leer etiquetas, guardar etiquetas y realizar busquedas.

Antes de optimizar, se necesita medir tiempos reales por operacion para evitar cambios prematuros o incorrectos.

## Archivos modificados

- `app/core/config.py`
- `app/gui/customtk_window.py`
- `app/services/image_service.py`
- `app/services/metadata_service.py`
- `docs/desarrollo/fase-18-mediciones-rendimiento.md`
- `opencode-logs/fase-18-mediciones-rendimiento-log.md`

## Que operaciones se miden

En la GUI principal:

- `abrir_carpeta()`.
- Cantidad de imagenes encontradas al abrir carpeta.
- `mostrar_imagen()` total.
- `renderizar_imagen_actual()`.
- Lectura de etiquetas dentro de `mostrar_imagen()`.
- `guardar_etiquetas()` total.
- Lectura previa de etiquetas dentro de `guardar_etiquetas()`.
- Escritura de etiquetas dentro de `guardar_etiquetas()`.
- `buscar_por_etiqueta()` total.
- Cantidad de imagenes revisadas durante busqueda.
- Cantidad de resultados encontrados.
- `limpiar_busqueda()`.
- Redimensionamiento de imagen.

En servicios:

- `buscar_imagenes()`.
- Cantidad de imagenes encontradas.
- `cargar_imagen()`.
- `leer_etiquetas()`.
- `escribir_etiquetas()`.
- Tiempo interno de ExifTool por accion.

## Formato de salida

Las mediciones salen por consola con prefijo `[PERF]`.

Ejemplos:

```text
[PERF] buscar_imagenes - imagenes encontradas: 125
[PERF] buscar_imagenes: 0.420s
[PERF] abrir_carpeta - imagenes encontradas: 125
[PERF] abrir_carpeta: 0.750s
[PERF] cargar_imagen: 0.180s
[PERF] renderizar_imagen_actual: 0.230s
[PERF] exiftool leer las etiquetas: 0.310s
[PERF] leer_etiquetas: 0.315s
[PERF] mostrar_imagen leer_etiquetas: 0.315s
[PERF] mostrar_imagen total: 0.580s
[PERF] buscar_por_etiqueta - imagenes revisadas: 125
[PERF] buscar_por_etiqueta - resultados: 4
[PERF] buscar_por_etiqueta total: 9.800s
```

## Control de mediciones

Se agrego `DEBUG_RENDIMIENTO = True` en `app/core/config.py`.

Esto permite desactivar las mediciones temporalmente cambiando ese valor a `False` en una fase futura. En esta fase queda activado porque el objetivo es recopilar datos.

## Como ejecutar pruebas en desarrollo

Ejecutar:

```powershell
.\venv\Scripts\python.exe main.py
```

Luego observar la salida `[PERF]` en la consola mientras se prueban las operaciones principales.

## Como ejecutar pruebas en el exe

Despues de reconstruir el `.exe`, ejecutar:

```powershell
.\dist\EtiquetadorImagenes\EtiquetadorImagenes.exe
```

Si se necesita ver la salida `[PERF]`, conviene ejecutar desde una consola o generar una variante de build con consola en una fase posterior de diagnostico. En el build actual `--windowed`, la salida de `print()` puede no verse en una consola normal.

## Pruebas manuales recomendadas

En desarrollo:

- Abrir carpeta pequena.
- Abrir carpeta grande.
- Navegar entre 10 imagenes.
- Buscar etiqueta existente.
- Buscar etiqueta inexistente.
- Guardar etiquetas en una copia de prueba.
- Limpiar busqueda.

En el build `.exe` reconstruido:

- Abrir carpeta pequena.
- Abrir carpeta grande.
- Navegar entre 10 imagenes.
- Buscar etiqueta existente.
- Buscar etiqueta inexistente.
- Guardar etiquetas en una copia de prueba.
- Limpiar busqueda.

## Como interpretar resultados

- Si `buscar_imagenes()` es alto, el cuello de botella esta en recorrido de carpetas, cantidad de archivos, OneDrive o disco.
- Si `cargar_imagen()` es alto, el cuello de botella esta en Pillow, tamano de imagen, disco o descarga bajo demanda.
- Si `renderizar_imagen_actual()` es alto, revisar carga, resize y creacion de `ImageTk.PhotoImage`.
- Si `leer_etiquetas()` o `exiftool leer las etiquetas` es alto, ExifTool y el arranque de procesos externos son candidatos a optimizacion.
- Si `buscar_por_etiqueta total` crece proporcionalmente a la cantidad de imagenes, conviene cachear etiquetas o crear un indice temporal.
- Si `guardar_etiquetas()` es alto, separar lectura previa, confirmacion y escritura para identificar donde se va el tiempo.

## Alcance

Esta fase solo agrega mediciones temporales. No se optimizo la carga de imagenes, no se redujeron llamadas a ExifTool, no se agrego cache, no se agrego threading y no se cambio el empaquetado.

No se hizo commit.
