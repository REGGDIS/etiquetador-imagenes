# Fase 14 - Preview de imagenes en CustomTkinter

## Objetivo

Mejorar el tamaño real de previsualizacion de imagenes en la interfaz principal CustomTkinter, permitiendo que solicite una imagen mas grande al servicio sin afectar la GUI Tkinter legacy.

## Problema detectado

`app/services/image_service.py` reducia siempre las imagenes con `IMAGE_PREVIEW_SIZE = (700, 500)` antes de devolverlas. Como `app/gui/customtk_window.py` usaba esa misma funcion sin parametros, CustomTkinter recibia una imagen ya limitada aunque su panel principal pudiera mostrar una previsualizacion mas grande.

Durante pruebas manuales posteriores se detecto tambien que algunas fotos de celular no respetaban la orientacion EXIF y que algunas imagenes horizontales o verticales grandes podian verse cortadas dentro del visor basado en `CTkLabel`.

## Archivos modificados

- `app/core/config.py`.
- `app/services/image_service.py`.
- `app/gui/customtk_window.py`.
- `docs/desarrollo/fase-14-preview-imagenes-customtkinter.md`.

## Cambios realizados

- Se mantuvo `IMAGE_PREVIEW_SIZE = (700, 500)` como valor por defecto para compatibilidad.
- Se agrego `CUSTOMTK_IMAGE_PREVIEW_SIZE = (1400, 1000)` para la previsualizacion principal de CustomTkinter.
- `cargar_imagen()` ahora acepta `max_size` opcional y usa `IMAGE_PREVIEW_SIZE` cuando no se pasa ningun valor.
- `cargar_imagen()` aplica `ImageOps.exif_transpose()` antes de generar la miniatura para respetar la orientacion EXIF.
- CustomTkinter ahora llama a `cargar_imagen(ruta_imagen, CUSTOMTK_IMAGE_PREVIEW_SIZE)` en `mostrar_imagen()`.
- CustomTkinter tambien usa el mismo tamano mayor en `_redimensionar_imagen_actual()`.
- El visor principal de imagen en CustomTkinter se cambio de `CTkLabel`/`CTkImage` a un `tk.Canvas` dentro del panel izquierdo.
- El Canvas dibuja placeholders centrados cuando no hay imagen o no hay resultados.
- La imagen se ajusta con una logica tipo `contain` usando el area disponible del Canvas antes de convertirla a `ImageTk.PhotoImage`.
- La imagen se dibuja centrada en el Canvas con `create_image(..., anchor="center")`.

## Decisiones tecnicas

- Se evita aumentar globalmente `IMAGE_PREVIEW_SIZE` para no cambiar el comportamiento de la GUI legacy.
- Se mantiene `thumbnail()` para conservar proporcion y evitar cargar imagenes sin limite en la GUI.
- Se mantiene `with Image.open(...)` y `return imagen.copy()` para cerrar correctamente el archivo abierto por Pillow.
- Se aplica la orientacion EXIF en el servicio de imagenes para que todas las interfaces reciban la imagen con orientacion corregida.
- CustomTkinter calcula la escala con ancho y alto disponibles del frame de imagen, usando `min(..., 1)` para evitar ampliar artificialmente imagenes pequenas.
- CustomTkinter redimensiona la imagen PIL al tamano final antes de crear `ImageTk.PhotoImage`, para evitar recortes por diferencias entre el tamano solicitado y el area visible del widget.
- Se reemplazo el visor basado en `CTkLabel` porque podia recortar imagenes grandes aunque la imagen PIL ya estuviera redimensionada.
- Se evita duplicar funciones de carga de imagen.
- Se deja a CustomTkinter decidir que necesita una previsualizacion mayor, mientras el servicio conserva un valor seguro por defecto.

## Que se mantuvo intacto

- `main.py`.
- `main_customtk.py`.
- `main_tkinter_legacy.py`.
- `app/gui/legacy/tkinter_window.py`.
- `app/services/metadata_service.py`.
- `app/services/tag_service.py`.
- `requirements.txt`.
- `.gitignore`.
- `README.md`.
- `exiftool.exe`.
- `exiftool_files/`.
- La lectura y escritura real de metadatos `Keywords` con ExifTool.
- La busqueda por etiquetas.
- La normalizacion de etiquetas.

## Verificaciones ejecutadas

- `git status --short` al inicio.
- `.\venv\Scripts\python.exe -B -c "import main"`.
- `.\venv\Scripts\python.exe -B -c "import main_customtk"`.
- `.\venv\Scripts\python.exe -B -c "import main_tkinter_legacy"`.
- `.\venv\Scripts\python.exe -B -c "from app.services.image_service import cargar_imagen; print('image_service OK')"`.
- `git diff -- app/core/config.py app/services/image_service.py app/gui/customtk_window.py docs/desarrollo/fase-14-preview-imagenes-customtkinter.md`.
- `git diff --no-index -- /dev/null docs/desarrollo/fase-14-preview-imagenes-customtkinter.md`.
- `git status --short`.

## Pruebas manuales recomendadas

1. Ejecutar `.\venv\Scripts\python.exe main.py`.
2. Abrir una carpeta con fotos verticales tomadas con celular.
3. Confirmar que ya no aparecen giradas.
4. Abrir fotos horizontales grandes.
5. Confirmar que ya no se cortan.
6. Abrir imagenes pequenas.
7. Confirmar que no se agrandan artificialmente de forma exagerada.
8. Redimensionar la ventana.
9. Confirmar que la imagen se ajusta sin errores.
10. Navegar rapido entre imagenes.
11. Buscar una etiqueta existente.
12. Guardar etiquetas y verificar que ExifTool sigue escribiendo `Keywords`.
13. Ejecutar `.\venv\Scripts\python.exe main_tkinter_legacy.py`.
14. Confirmar que la GUI legacy abre, carga imagenes y navega correctamente.

## Estado final

- `cargar_imagen()` conserva compatibilidad con llamadas existentes.
- Las imagenes cargadas respetan la orientacion EXIF cuando existe.
- CustomTkinter usa una previsualizacion mayor mediante `CUSTOMTK_IMAGE_PREVIEW_SIZE`.
- CustomTkinter renderiza la imagen en un Canvas, centrada y ajustada al area visible, por lo que fotos verticales y horizontales grandes deben verse completas sin recorte.
- La GUI legacy sigue usando el tamano por defecto sin cambios.
- No se modifico ExifTool.
- No se modifico la lectura/escritura de `Keywords`.
- No se agregaron dependencias.
- No se hizo commit.
