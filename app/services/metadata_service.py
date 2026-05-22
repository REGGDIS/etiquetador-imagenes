import subprocess

from app.core.config import EXIFTOOL_PATH


def leer_etiquetas(ruta_imagen):
    resultado = subprocess.run(
        [EXIFTOOL_PATH, "-keywords", "-s3", ruta_imagen],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    return resultado.stdout.strip().split("\n") if resultado.stdout.strip() else []


def escribir_etiquetas(ruta_imagen, etiquetas):
    comando = [EXIFTOOL_PATH]
    comando += [f"-keywords={etiqueta}" for etiqueta in etiquetas]
    comando += ["-overwrite_original", ruta_imagen]

    subprocess.run(comando, check=True)
