import os

from PIL import Image
from PIL import ImageOps
from PIL import UnidentifiedImageError

from app.core.config import IMAGE_PREVIEW_SIZE, SUPPORTED_IMAGE_EXTENSIONS


def buscar_imagenes(carpeta):
    imagenes = []
    for root_dir, _, files in os.walk(carpeta):
        for nombre_archivo in files:
            if nombre_archivo.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
                imagenes.append(os.path.join(root_dir, nombre_archivo))
    imagenes.sort()
    return imagenes


def cargar_imagen(ruta_imagen, max_size=IMAGE_PREVIEW_SIZE):
    try:
        with Image.open(ruta_imagen) as imagen:
            imagen = ImageOps.exif_transpose(imagen)
            imagen.thumbnail(max_size)
            return imagen.copy()
    except (OSError, UnidentifiedImageError, ValueError) as error:
        raise RuntimeError(f"No se pudo abrir la imagen.\n{error}") from error
