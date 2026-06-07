# Fase 17 - Adaptar rutas para empaquetado

## Objetivo

Preparar la resolucion de rutas de la aplicacion para que pueda encontrar `exiftool.exe` tanto en modo desarrollo como en un futuro empaquetado con PyInstaller en modo `onedir`.

## Problema detectado

Antes de esta fase, `app/core/config.py` calculaba `BASE_DIR` desde la ubicacion del archivo `config.py`. Ese enfoque funciona al ejecutar `python main.py` desde el proyecto, pero puede fallar en una aplicacion congelada porque la ubicacion real de los recursos cambia al generar un `.exe`.

## Archivos modificados

- `app/core/config.py`
- `app/services/metadata_service.py`
- `docs/desarrollo/fase-17-adaptar-rutas-empaquetado.md`
- `opencode-logs/fase-17-adaptar-rutas-empaquetado-log.md`

## Decision tecnica

Se agrego una funcion `obtener_base_app()` en `app/core/config.py` para centralizar la resolucion de la ruta base.

La funcion usa dos estrategias:

- En modo desarrollo, calcula la raiz del proyecto a partir de `app/core/config.py`.
- En modo PyInstaller congelado, usa `os.path.dirname(sys.executable)`, que corresponde a la carpeta donde estara el ejecutable en un build `onedir`.

Tambien se agrego `EXIFTOOL_FILES_DIR` para dejar definida la ubicacion esperada de `exiftool_files/` junto a `exiftool.exe`.

## Resolucion de ruta en desarrollo

Cuando la app se ejecuta con Python normal, por ejemplo:

```powershell
python main.py
```

`getattr(sys, "frozen", False)` es falso y `BASE_DIR` sigue apuntando a la raiz del proyecto.

Por lo tanto, las rutas esperadas continuan siendo:

```text
<raiz-del-proyecto>/exiftool.exe
<raiz-del-proyecto>/exiftool_files/
```

## Resolucion de ruta en PyInstaller onedir

Cuando la app este empaquetada y congelada por PyInstaller, `getattr(sys, "frozen", False)` sera verdadero.

En ese caso, `BASE_DIR` apuntara a:

```python
os.path.dirname(sys.executable)
```

Para un build `onedir`, la estructura esperada sera similar a:

```text
dist/EtiquetadorImagenes/EtiquetadorImagenes.exe
dist/EtiquetadorImagenes/exiftool.exe
dist/EtiquetadorImagenes/exiftool_files/
```

## Que se mantuvo intacto

- No se genero `.exe`.
- No se instalo PyInstaller.
- No se creo archivo `.spec`.
- No se modifico `exiftool.exe`.
- No se modifico `exiftool_files/`.
- No se modifico `requirements.txt`.
- No se modifico `.gitignore`.
- No se modifico la GUI principal.
- No se modifico la GUI legacy.
- No se modificaron los servicios de imagenes ni normalizacion de etiquetas.
- No se cambio la logica de lectura o escritura de metadatos.

## Verificaciones ejecutadas

```powershell
.\venv\Scripts\python.exe -B -c "import main"
.\venv\Scripts\python.exe -B -c "import main_customtk"
.\venv\Scripts\python.exe -B -c "import main_tkinter_legacy"
.\venv\Scripts\python.exe -B -c "from app.core.config import BASE_DIR, EXIFTOOL_PATH, EXIFTOOL_FILES_DIR; print(BASE_DIR); print(EXIFTOOL_PATH); print(EXIFTOOL_FILES_DIR)"
.\venv\Scripts\python.exe -B -c "from app.services.metadata_service import validar_exiftool; validar_exiftool(); print('exiftool OK')"
```

## Pruebas manuales recomendadas

- Ejecutar `python main.py` en desarrollo.
- Abrir una carpeta con imagenes.
- Verificar que se muestren imagenes horizontales y verticales.
- Leer etiquetas existentes desde metadatos `Keywords`.
- Guardar etiquetas en una copia de prueba.
- Confirmar que la proteccion contra borrado accidental sigue funcionando.
- Probar rutas con espacios y caracteres especiales.
- Probar imagenes ubicadas dentro y fuera de OneDrive.

## Estado final

La aplicacion mantiene compatibilidad con desarrollo y queda preparada para buscar `exiftool.exe` junto al ejecutable en un futuro build PyInstaller `onedir`.

No se genero `.exe` y no se hizo commit.
