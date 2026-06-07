import os
from time import perf_counter

from PIL import Image
from PIL import ImageOps
from PIL import UnidentifiedImageError

from app.core.config import DEBUG_RENDIMIENTO, IMAGE_PREVIEW_SIZE, SUPPORTED_IMAGE_EXTENSIONS


def _medir_tiempo(nombre, inicio):
    if DEBUG_RENDIMIENTO:
        print(f"[PERF] {nombre}: {perf_counter() - inicio:.3f}s")


def buscar_imagenes(carpeta):
    inicio = perf_counter()
    imagenes = []
    for root_dir, _, files in os.walk(carpeta):
        for nombre_archivo in files:
            if nombre_archivo.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
                imagenes.append(os.path.join(root_dir, nombre_archivo))
    imagenes.sort()
    if DEBUG_RENDIMIENTO:
        print(f"[PERF] buscar_imagenes - imagenes encontradas: {len(imagenes)}")
    _medir_tiempo("buscar_imagenes", inicio)
    return imagenes


def cargar_imagen(ruta_imagen, max_size=IMAGE_PREVIEW_SIZE):
    inicio = perf_counter()
    try:
        with Image.open(ruta_imagen) as imagen:
            imagen = ImageOps.exif_transpose(imagen)
            imagen.thumbnail(max_size)
            return imagen.copy()
    except (OSError, UnidentifiedImageError, ValueError) as error:
        raise RuntimeError(f"No se pudo abrir la imagen.\n{error}") from error
    finally:
        _medir_tiempo("cargar_imagen", inicio)
