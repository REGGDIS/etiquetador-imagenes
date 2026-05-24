# Fase 7 - Busqueda interna por etiquetas

## Objetivo

Implementar una busqueda interna basica por etiquetas en las imagenes cargadas, usando los metadatos reales `Keywords` leidos con ExifTool y normalizando el texto de busqueda con el servicio de etiquetas existente.

## Archivos modificados

- `app/gui/main_window.py`
- `docs/desarrollo/fase-7-busqueda-etiquetas.md`

No se modifico `app/services/tag_service.py` porque la funcion `normalizar_texto_etiqueta()` ya cubria la necesidad de normalizacion para busqueda.

## Cambios realizados

- Se agrego estado interno para busqueda:
  - `self.lista_imagenes_filtrada`
  - `self.busqueda_activa`
  - `self.texto_busqueda_actual`
- Se agrego el helper `obtener_lista_actual()` para centralizar si la navegacion usa la lista completa o la lista filtrada.
- Se agregaron controles visuales minimos:
  - etiqueta `Buscar por etiqueta:`
  - campo de busqueda
  - boton `Buscar`
  - boton `Limpiar busqueda`
- Se implemento busqueda exacta normalizada sobre etiquetas reales `Keywords`.
- Se adapto la navegacion para operar sobre la lista visible actual.
- Se adapto el contador para reflejar la lista actual.
- Se adapto el estado de botones segun existan imagenes visibles, imagenes cargadas y busqueda activa.
- Se agrego manejo de busqueda sin resultados.
- Se agrego manejo de errores de ExifTool durante busqueda sin interrumpir todo el proceso.
- Se mantuvo el guardado real de etiquetas en `Keywords`.
- Si se guardan etiquetas durante una busqueda activa, se informa que se debe repetir la busqueda para actualizar resultados.

## Decisiones tecnicas tomadas

- La busqueda se implemento dentro de `app/gui/main_window.py` para mantener la fase incremental y evitar crear un servicio prematuro.
- `self.lista_imagenes` se mantiene como lista completa de imagenes cargadas.
- `self.lista_imagenes_filtrada` contiene solo los resultados de la busqueda activa.
- `self.busqueda_activa` define explicitamente si la app navega sobre resultados filtrados.
- La coincidencia es exacta y normalizada: `perro` coincide con `perro`, pero no con `per`.
- No se implemento threading en esta fase para evitar complejidad adicional en Tkinter.
- No se creo cache persistente, base de datos ni archivo JSON.
- No se agregaron dependencias externas.

## Verificaciones ejecutadas

- `.\venv\Scripts\python.exe -B -c "import main"`: OK, sin salida.
- `.\venv\Scripts\python.exe -B -c "from app.services.tag_service import normalizar_texto_etiqueta; assert normalizar_texto_etiqueta('PÉRRO') == 'perro'; print('OK')"`: OK.
- `git diff -- app/gui/main_window.py app/services/tag_service.py docs/desarrollo/fase-7-busqueda-etiquetas.md`: ejecutado.
- `git status --short`: ejecutado.

## Pruebas manuales recomendadas

1. Ejecutar `.\venv\Scripts\python.exe main.py`.
2. Abrir una carpeta con imagenes.
3. Buscar una etiqueta existente, por ejemplo `perro`.
4. Confirmar que la navegacion queda limitada a las imagenes coincidentes.
5. Confirmar que el contador muestra el total filtrado.
6. Buscar una etiqueta inexistente.
7. Confirmar que aparece el estado `Sin resultados`.
8. Limpiar busqueda.
9. Confirmar que vuelve la lista completa.
10. Guardar etiquetas durante una busqueda activa y confirmar que se mantiene el comportamiento esperado.

## Estado final de Git

Estado observado despues de la implementacion:

- `M app/gui/main_window.py`
- `?? docs/desarrollo/`

## Commit

No se hizo commit.
