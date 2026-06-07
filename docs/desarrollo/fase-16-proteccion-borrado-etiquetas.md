# Fase 16 - Proteccion contra borrado accidental de etiquetas

## Objetivo

Evitar que la aplicacion borre etiquetas reales existentes en metadatos `Keywords` cuando el usuario guarda con el campo de etiquetas vacio sin haber confirmado esa accion.

## Problema detectado

Durante pruebas con carpetas en OneDrive se observo que Windows/OneDrive podia no mostrar etiquetas hasta que ExifTool leyera los archivos. Aunque las etiquetas no estaban borradas, quedo expuesto un riesgo real: guardar con el campo vacio podia sobrescribir `Keywords` con una lista vacia y eliminar etiquetas existentes.

## Archivos modificados

- `app/gui/customtk_window.py`.
- `docs/desarrollo/fase-16-proteccion-borrado-etiquetas.md`.

## Cambios realizados

- Se actualizo `guardar_etiquetas()` para leer las etiquetas reales existentes con `leer_etiquetas(ruta_imagen)` antes de escribir metadatos.
- Se mantiene la lectura del campo `CTkTextbox` mediante `obtener_texto_etiquetas()`, que usa indices `"1.0"` y `"end"`.
- Se mantiene la normalizacion existente con `normalizar_etiquetas_desde_texto()`.
- Si el campo queda vacio y la imagen tiene etiquetas existentes, se muestra una confirmacion con `messagebox.askyesno`.
- Si el usuario cancela, no se llama a `escribir_etiquetas()` y se informa que las etiquetas existentes se conservaron.
- Si el usuario confirma, se permite escribir la lista vacia para eliminar las etiquetas.
- Si no existen etiquetas previas y el campo esta vacio, se evita una escritura innecesaria y se muestra el estado `No hay etiquetas para guardar.`.
- Si ExifTool no puede leer las etiquetas existentes antes de guardar, se cancela el guardado para no asumir que la imagen no tiene etiquetas.

## Decisiones tecnicas

- La proteccion se basa en una lectura real previa de metadatos con ExifTool, no en el contenido visible del campo ni en una cache de estado.
- `MetadataError` al verificar etiquetas existentes se trata como condicion segura: se muestra error y no se sobrescriben metadatos.
- No se modificaron los servicios de metadatos ni de etiquetas porque las funciones existentes cubren el comportamiento necesario.
- No se agregaron dependencias ni almacenamiento adicional.
- En busqueda activa se conserva el mensaje existente despues de guardar: `Etiquetas guardadas. Repite la busqueda si quieres actualizar los resultados.`

## Comportamiento esperado

- Si la imagen tiene etiquetas existentes y el campo esta vacio, la app pide confirmacion antes de borrar.
- Si el usuario elige `No`, no se escriben metadatos y el estado indica que el guardado fue cancelado.
- Si el usuario elige `Si`, se permite eliminar las etiquetas existentes.
- Si la imagen no tiene etiquetas existentes y el campo esta vacio, no se pide confirmacion y no se ejecuta una escritura innecesaria.
- Si el campo contiene etiquetas, el guardado funciona como antes, con normalizacion y escritura real en `Keywords`.
- Si hay busqueda activa, los resultados no se recalculan automaticamente despues de guardar.

## Verificaciones ejecutadas

- `git status --short` al inicio.
- `.\venv\Scripts\python.exe -B -c "import main"`.
- `.\venv\Scripts\python.exe -B -c "import main_customtk"`.
- `.\venv\Scripts\python.exe -B -c "import main_tkinter_legacy"`.
- `git diff -- app/gui/customtk_window.py docs/desarrollo/fase-16-proteccion-borrado-etiquetas.md`.
- `git diff --no-index -- /dev/null docs/desarrollo/fase-16-proteccion-borrado-etiquetas.md`.
- `git status --short`.

## Pruebas manuales recomendadas

1. Ejecutar `.\venv\Scripts\python.exe main.py`.
2. Abrir una carpeta con imagenes.
3. Seleccionar una imagen que ya tenga etiquetas.
4. Borrar todo el contenido del campo de etiquetas.
5. Presionar `Guardar etiquetas`.
6. Confirmar que aparece la advertencia de borrado.
7. Elegir `No` y verificar que las etiquetas no se borran.
8. Repetir y elegir `Si` usando una imagen de prueba o una copia, confirmando que se permite eliminar etiquetas.
9. Seleccionar una imagen sin etiquetas y probar guardar vacio.
10. Seleccionar una imagen con etiquetas normales y guardar cambios.
11. Verificar con ExifTool: `.\exiftool.exe -keywords -s3 "C:\ruta\a\imagen.jpg"`.
12. Confirmar que busqueda, navegacion y limpieza de busqueda siguen funcionando.
13. Ejecutar `.\venv\Scripts\python.exe main_tkinter_legacy.py`.
14. Confirmar que la GUI legacy sigue abriendo correctamente.

## Estado final

- La app no borra etiquetas existentes sin confirmacion.
- Si el usuario cancela, no se escriben metadatos.
- Si el usuario confirma, se permite eliminar etiquetas.
- El guardado normal de etiquetas sigue usando ExifTool y la normalizacion existente.
- No se modifico ExifTool.
- No se modificaron servicios.
- No se modificaron entradas principales.
- No se agregaron dependencias.
- No se hizo commit.
