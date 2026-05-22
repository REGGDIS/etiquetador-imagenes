# Guía de instalación de ExifTool en Windows

Esta guía explica cómo instalar ExifTool localmente para el proyecto **Etiquetador de Imágenes** en Windows.

## Qué es ExifTool en este proyecto

ExifTool es la herramienta que usa la aplicación para leer y escribir metadatos reales en las imágenes.

En este proyecto se utiliza específicamente para:

- Leer etiquetas existentes desde el campo `Keywords`.
- Guardar nuevas etiquetas en el campo `Keywords`.
- Permitir que esas etiquetas puedan usarse posteriormente en búsquedas desde el Explorador de Windows.

La aplicación espera encontrar ExifTool como un archivo local llamado `exiftool.exe` en la raíz del proyecto.

## Requisitos

- Usar Windows.
- Tener el proyecto clonado localmente.
- Tener Python instalado.
- Tener creado y funcionando el entorno virtual del proyecto.
- Tener acceso al archivo descargado de ExifTool para Windows.

## Descargar ExifTool

Descarga ExifTool desde el sitio oficial:

https://exiftool.org/

Normalmente, para Windows se descarga un archivo comprimido. No uses enlaces no oficiales ni copias de origen desconocido.

## Instalación local para este proyecto

1. Descarga ExifTool para Windows desde el sitio oficial.
2. Descomprime el archivo descargado.
3. Ubica el ejecutable incluido en la descarga.
4. Si el ejecutable viene con otro nombre similar, renómbralo a `exiftool.exe`.
5. Copia `exiftool.exe` a la raíz del proyecto, junto a `main.py`.
6. Si la descarga incluye o genera una carpeta `exiftool_files/`, cópiala también a la raíz del proyecto.

## Estructura esperada después de instalar

La raíz del proyecto debería quedar similar a esto:

```text
etiquetador-imagenes/
├── main.py
├── app/
├── README.md
├── requirements.txt
├── exiftool.exe
└── exiftool_files/
```

## Verificación desde PowerShell

Abre PowerShell en la raíz del proyecto y ejecuta:

```powershell
.\exiftool.exe -ver
```

Si ExifTool está correctamente ubicado, el comando debería mostrar un número de versión.

## Verificación con una imagen

Para leer las etiquetas `Keywords` de una imagen, ejecuta:

```powershell
.\exiftool.exe -keywords -s3 "C:\ruta\a\imagen.jpg"
```

Si la imagen tiene etiquetas guardadas en `Keywords`, deberían mostrarse en la consola.

## Problemas comunes

### `exiftool.exe` no se reconoce

Este error suele aparecer si PowerShell no está ubicado en la raíz del proyecto o si el archivo no está en esa carpeta.

Verifica que estás ejecutando el comando desde la carpeta donde está `main.py` y usa:

```powershell
.\exiftool.exe -ver
```

### El archivo no está en la raíz del proyecto

La aplicación busca `exiftool.exe` junto a `main.py`. Si está en otra carpeta, la app no lo encontrará.

### El ejecutable tiene otro nombre

Algunas descargas pueden traer un nombre similar. Renombra el ejecutable a exactamente:

```text
exiftool.exe
```

### PowerShell está ubicado en otra carpeta

Antes de ejecutar comandos de verificación, entra a la carpeta del proyecto:

```powershell
cd ruta\al\proyecto\etiquetador-imagenes
```

### La app muestra que no encontró ExifTool

Confirma que existe este archivo:

```text
etiquetador-imagenes\exiftool.exe
```

También verifica que no esté dentro de una subcarpeta por error.

### OneDrive puede bloquear archivos temporalmente

Si el proyecto está dentro de OneDrive, puede haber demoras de sincronización o bloqueos temporales. Espera a que termine la sincronización o prueba ejecutar la app nuevamente.

### Advertencias del antivirus

Algunos antivirus pueden mostrar advertencias con ejecutables descargados. Descarga ExifTool solo desde el sitio oficial y evita archivos de terceros.

## Recomendación sobre rutas

El proyecto espera que `exiftool.exe` esté en la raíz, junto a `main.py`.

Después de configurarlo, evita mover `exiftool.exe` o `exiftool_files/`. Si aparecen problemas, usa una ruta de proyecto simple y evita carpetas con estructuras demasiado largas o complejas.

## Nota sobre Git

`exiftool.exe` y `exiftool_files/` no deben subirse a GitHub.

Estos archivos están ignorados por `.gitignore` porque son dependencias locales de ejecución. Cada usuario del proyecto debe instalar ExifTool localmente en su equipo.
