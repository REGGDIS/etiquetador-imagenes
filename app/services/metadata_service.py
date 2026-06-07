import os
import subprocess
from os import path
from time import perf_counter

from app.core.config import BASE_DIR, DEBUG_RENDIMIENTO, EXIFTOOL_LIB_DIR, EXIFTOOL_PATH


def _medir_tiempo(nombre, inicio):
    if DEBUG_RENDIMIENTO:
        print(f"[PERF] {nombre}: {perf_counter() - inicio:.3f}s")


class MetadataError(RuntimeError):
    pass


def validar_exiftool():
    if not path.isfile(EXIFTOOL_PATH):
        raise MetadataError(
            "No se encontró exiftool.exe.\n"
            f"Ruta esperada: {EXIFTOOL_PATH}"
        )
    if not path.isdir(EXIFTOOL_LIB_DIR):
        raise MetadataError(
            "No se encontró la carpeta interna de librerías de ExifTool.\n"
            f"Ruta esperada: {EXIFTOOL_LIB_DIR}"
        )


def _crear_entorno_exiftool():
    env = os.environ.copy()
    env["PERL5LIB"] = EXIFTOOL_LIB_DIR
    return env


def _ejecutar_exiftool(argumentos, accion):
    validar_exiftool()
    inicio = perf_counter()

    try:
        return subprocess.run(
            [EXIFTOOL_PATH, *argumentos],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            env=_crear_entorno_exiftool(),
            cwd=BASE_DIR,
        )
    except subprocess.CalledProcessError as error:
        detalle = (error.stderr or error.stdout or "").strip()
        if not detalle:
            detalle = f"ExifTool terminó con código {error.returncode}."
        raise MetadataError(f"No se pudo {accion} con ExifTool.\n{detalle}") from error
    except OSError as error:
        raise MetadataError(f"No se pudo ejecutar ExifTool.\n{error}") from error
    finally:
        _medir_tiempo(f"exiftool {accion}", inicio)


def leer_etiquetas(ruta_imagen):
    inicio = perf_counter()
    resultado = _ejecutar_exiftool(
        ["-keywords", "-s3", ruta_imagen],
        "leer las etiquetas"
    )
    etiquetas = resultado.stdout.strip().splitlines() if resultado.stdout.strip() else []
    _medir_tiempo("leer_etiquetas", inicio)
    return etiquetas


def escribir_etiquetas(ruta_imagen, etiquetas):
    inicio = perf_counter()
    argumentos = [f"-keywords={etiqueta}" for etiqueta in etiquetas]
    argumentos += ["-overwrite_original", ruta_imagen]

    try:
        _ejecutar_exiftool(argumentos, "guardar las etiquetas")
    finally:
        _medir_tiempo("escribir_etiquetas", inicio)
