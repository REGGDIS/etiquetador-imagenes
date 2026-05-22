import os

from PIL import Image

from app.core.config import IMAGE_PREVIEW_SIZE, SUPPORTED_IMAGE_EXTENSIONS


def buscar_imagenes(carpeta):
    imagenes = []
    for root_dir, _, files in os.walk(carpeta):
        for nombre_archivo in files:
            if nombre_archivo.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
                imagenes.append(os.path.join(root_dir, nombre_archivo))
    imagenes.sort()
    return imagenes


def cargar_imagen(ruta_imagen):
    imagen = Image.open(ruta_imagen)
    imagen.thumbnail(IMAGE_PREVIEW_SIZE)
    return imagen
