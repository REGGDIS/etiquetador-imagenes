# Fase 17 - Primer build exe

## Objetivo

Crear el primer empaquetado `.exe` de la aplicacion en modo `onedir` usando PyInstaller, incluyendo `exiftool.exe`, `exiftool_files/` y recursos internos de CustomTkinter.

## Herramienta usada

Se uso PyInstaller instalado localmente en el entorno virtual del proyecto.

Version instalada:

```text
PyInstaller 6.20.0
```

PyInstaller no estaba instalado al inicio de la fase, por lo que se instalo solo dentro de `venv/` con:

```powershell
.\venv\Scripts\python.exe -m pip install pyinstaller
```

No se modifico `requirements.txt`, porque PyInstaller queda tratado por ahora como herramienta local de desarrollo.

## Por que se uso onedir

Se uso `onedir` porque la aplicacion depende de un binario externo (`exiftool.exe`) y de una carpeta auxiliar (`exiftool_files/`).

Este formato permite inspeccionar facilmente que ambos recursos queden incluidos junto al ejecutable y reduce riesgos frente a `onefile`, como extraccion temporal, antivirus y rutas internas mas dificiles de depurar.

## Comando PyInstaller usado

El primer comando ejecutado fue:

```powershell
.\venv\Scripts\pyinstaller.exe --noconfirm --clean --windowed --onedir --name "EtiquetadorImagenes" --collect-data customtkinter --add-binary "exiftool.exe;." --add-data "exiftool_files;exiftool_files" main.py
```

Con PyInstaller 6, ese build dejo los archivos de soporte dentro de `_internal`, por lo que `exiftool.exe` no quedo junto a `EtiquetadorImagenes.exe`.

Para cumplir la decision de rutas tomada en la fase anterior, se reconstruyo usando `--contents-directory "."`:

```powershell
.\venv\Scripts\pyinstaller.exe --noconfirm --clean --windowed --onedir --contents-directory "." --name "EtiquetadorImagenes" --collect-data customtkinter --add-binary "exiftool.exe;." --add-data "exiftool_files;exiftool_files" main.py
```

## Archivos incluidos

- `main.py` como punto de entrada.
- Paquete `app/` detectado por PyInstaller.
- Dependencias Python necesarias.
- Recursos internos de CustomTkinter mediante `--collect-data customtkinter`.
- `exiftool.exe` mediante `--add-binary`.
- `exiftool_files/` mediante `--add-data`.
- `exiftool_files/lib/` como libreria Perl interna usada por ExifTool.

## Estructura esperada de dist

La estructura final esperada y verificada es:

```text
dist/EtiquetadorImagenes/EtiquetadorImagenes.exe
dist/EtiquetadorImagenes/exiftool.exe
dist/EtiquetadorImagenes/exiftool_files/
```

Tambien se incluyen DLLs, carpetas de Tcl/Tk, Pillow, CustomTkinter y otros archivos necesarios para ejecutar la aplicacion sin Python instalado globalmente.

## Verificaciones ejecutadas

```powershell
git status --short
git branch --show-current
.\venv\Scripts\python.exe -m pip show pyinstaller
Test-Path -LiteralPath "exiftool.exe"
Test-Path -LiteralPath "exiftool_files"
.\venv\Scripts\python.exe -m pip install pyinstaller
.\venv\Scripts\pyinstaller.exe --noconfirm --clean --windowed --onedir --name "EtiquetadorImagenes" --collect-data customtkinter --add-binary "exiftool.exe;." --add-data "exiftool_files;exiftool_files" main.py
.\venv\Scripts\pyinstaller.exe --noconfirm --clean --windowed --onedir --contents-directory "." --name "EtiquetadorImagenes" --collect-data customtkinter --add-binary "exiftool.exe;." --add-data "exiftool_files;exiftool_files" main.py
Test-Path -LiteralPath "dist\EtiquetadorImagenes\EtiquetadorImagenes.exe"
Test-Path -LiteralPath "dist\EtiquetadorImagenes\exiftool.exe"
Test-Path -LiteralPath "dist\EtiquetadorImagenes\exiftool_files"
.\venv\Scripts\python.exe -B -c "import main"
.\venv\Scripts\python.exe -B -c "from app.services.metadata_service import validar_exiftool; validar_exiftool(); print('exiftool OK')"
.\venv\Scripts\python.exe -B -c "from app.core.config import EXIFTOOL_PATH, EXIFTOOL_FILES_DIR, EXIFTOOL_LIB_DIR; print(EXIFTOOL_PATH); print(EXIFTOOL_FILES_DIR); print(EXIFTOOL_LIB_DIR)"
```

Resultados relevantes:

```text
dist/EtiquetadorImagenes/EtiquetadorImagenes.exe: True
dist/EtiquetadorImagenes/exiftool.exe: True
dist/EtiquetadorImagenes/exiftool_files: True
dist/EtiquetadorImagenes/exiftool_files/lib/strict.pm: True
exiftool OK
```

Tambien se lanzo el ejecutable generado con `Start-Process`. El proceso inicio correctamente y luego fue detenido para no dejar la GUI abierta.

Se probo ExifTool empaquetado definiendo `PERL5LIB` manualmente desde PowerShell:

```powershell
$env:PERL5LIB = "C:\Users\reggd\OneDrive - Aiep\proyectos\etiquetador\dist\EtiquetadorImagenes\exiftool_files\lib"
.\dist\EtiquetadorImagenes\exiftool.exe -ver
Remove-Item Env:PERL5LIB
```

Resultado:

```text
13.29
```

## Problemas encontrados y soluciones

Problema encontrado:

PyInstaller 6 usa `_internal` por defecto en builds `onedir`. Con el comando inicial, `exiftool.exe` y `exiftool_files/` no quedaron junto a `EtiquetadorImagenes.exe`, que es la ubicacion esperada por la resolucion de rutas implementada en la fase anterior.

Solucion aplicada:

Se agrego `--contents-directory "."` al comando de PyInstaller para generar un layout plano dentro de `dist/EtiquetadorImagenes/`, dejando `exiftool.exe` y `exiftool_files/` junto al ejecutable.

Problema encontrado despues del primer arranque:

El ejecutable empaquetado abria correctamente, pero al intentar leer etiquetas ExifTool fallaba con:

```text
Can't locate strict.pm in @INC
BEGIN failed--compilation aborted
```

Se comprobo que `strict.pm` si estaba presente en:

```text
dist/EtiquetadorImagenes/exiftool_files/lib/strict.pm
```

La causa era que ExifTool se estaba ejecutando, pero Perl no tenia configurado `@INC` para encontrar sus librerias internas dentro de `exiftool_files/lib`.

Solucion aplicada:

La app ahora define `PERL5LIB` al ejecutar ExifTool desde `app/services/metadata_service.py`, apuntando a `EXIFTOOL_LIB_DIR`. Tambien se ejecuta el proceso con `cwd=BASE_DIR`.

En `app/core/config.py` se agrego:

```python
EXIFTOOL_LIB_DIR = os.path.join(EXIFTOOL_FILES_DIR, "lib")
```

Con esto, ExifTool encuentra `strict.pm` tanto en desarrollo como en el build PyInstaller `onedir`.

Problema operativo durante rebuild:

Windows/OneDrive bloqueo temporalmente artefactos generados en `build/` y `dist/`, provocando `PermissionError`. Se limpiaron manualmente solo carpetas generadas e ignoradas por Git y luego el build final se completo correctamente.

## Pruebas manuales recomendadas

- Abrir `dist/EtiquetadorImagenes/EtiquetadorImagenes.exe`.
- Abrir carpeta con imagenes.
- Visualizar imagenes horizontales y verticales.
- Leer etiquetas existentes.
- Buscar una etiqueta existente.
- Buscar una etiqueta inexistente.
- Limpiar busqueda.
- Guardar etiqueta en una copia de prueba.
- Verificar desde ExifTool o Explorador de Windows que `Keywords` se escribio correctamente.
- Probar la proteccion contra borrado accidental.
- Probar rutas con espacios y caracteres especiales.
- Probar imagenes dentro de OneDrive y fuera del proyecto.

## Estado final

Se genero el build `onedir` funcional en `dist/EtiquetadorImagenes/` y se corrigio la ejecucion de ExifTool configurando `PERL5LIB`.

No se cambio a `onefile`, no se modifico ExifTool, no se modifico `requirements.txt` y no se hizo commit. La unica modificacion de codigo fuente fue la necesaria para pasar `PERL5LIB` al ejecutar ExifTool.
