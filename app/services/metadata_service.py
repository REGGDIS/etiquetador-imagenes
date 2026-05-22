import subprocess
from os import path

from app.core.config import EXIFTOOL_PATH


class MetadataError(RuntimeError):
    pass


def _validar_exiftool():
    if not path.isfile(EXIFTOOL_PATH):
        raise MetadataError(
            "No se encontró exiftool.exe en la raíz del proyecto.\n"
            f"Ruta esperada: {EXIFTOOL_PATH}"
        )


def _ejecutar_exiftool(argumentos, accion):
    _validar_exiftool()

    try:
        return subprocess.run(
            [EXIFTOOL_PATH, *argumentos],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as error:
        detalle = (error.stderr or error.stdout or "").strip()
        if not detalle:
            detalle = f"ExifTool terminó con código {error.returncode}."
        raise MetadataError(f"No se pudo {accion} con ExifTool.\n{detalle}") from error
    except OSError as error:
        raise MetadataError(f"No se pudo ejecutar ExifTool.\n{error}") from error


def leer_etiquetas(ruta_imagen):
    resultado = _ejecutar_exiftool(
        ["-keywords", "-s3", ruta_imagen],
        "leer las etiquetas"
    )
    return resultado.stdout.strip().splitlines() if resultado.stdout.strip() else []


def escribir_etiquetas(ruta_imagen, etiquetas):
    argumentos = [f"-keywords={etiqueta}" for etiqueta in etiquetas]
    argumentos += ["-overwrite_original", ruta_imagen]

    _ejecutar_exiftool(argumentos, "guardar las etiquetas")
