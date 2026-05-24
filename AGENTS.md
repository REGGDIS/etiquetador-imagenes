# AGENTS.md - Etiquetador de Imágenes

## Contexto del proyecto

Este proyecto es una aplicación de escritorio para Windows llamada “Etiquetador de Imágenes”, desarrollada con Python 3.12, Tkinter, Pillow y ExifTool.

La aplicación permite abrir carpetas y subcarpetas, visualizar imágenes, navegar entre ellas, leer etiquetas reales desde metadatos `Keywords` y guardar etiquetas usando ExifTool.

## Restricciones generales

- Mantener compatibilidad con Windows.
- Mantener Tkinter.
- Mantener Pillow.
- Mantener ExifTool.
- Mantener escritura real en metadatos `Keywords`.
- No introducir base de datos salvo instrucción explícita.
- No volver a usar JSON como almacenamiento principal.
- No agregar dependencias externas sin justificarlo.
- No tocar `exiftool.exe`, `exiftool_files/` ni `venv/`.
- No hacer commits automáticamente.

## Flujo de trabajo

Antes de modificar archivos:

1. Revisar `git status --short`.
2. Inspeccionar archivos relevantes.
3. Presentar un plan breve.
4. Aplicar solo los cambios solicitados.
5. Ejecutar verificaciones mínimas.
6. Mostrar `git diff` y `git status --short`.

## Documentación de fases

Cuando una tarea corresponda a una fase de desarrollo, crear o actualizar un resumen técnico limpio en:

`docs/desarrollo/fase-X-nombre.md`

Ese archivo sí puede formar parte del repositorio si documenta:

- objetivo de la fase;
- archivos modificados;
- cambios realizados;
- decisiones técnicas;
- verificaciones ejecutadas;
- pruebas manuales recomendadas;
- estado final;
- aclaración de que no se hizo commit.

## Logs completos de OpenCode/Codex

Además de mostrar la respuesta final en terminal, guardar una copia completa de la respuesta final en:

`opencode-logs/fase-X-nombre-log.md`

Reglas para logs:

- `opencode-logs/` es una carpeta local ignorada por Git.
- Los logs completos son solo para revisión local.
- No agregar archivos de `opencode-logs/` al commit.
- Si no existe la carpeta `opencode-logs/`, crearla.
- Mantener el resumen limpio en `docs/desarrollo/` separado del log completo.
