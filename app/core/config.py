import os
import sys


def obtener_base_app():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


BASE_DIR = obtener_base_app()
EXIFTOOL_EXECUTABLE = "exiftool.exe"
EXIFTOOL_PATH = os.path.join(BASE_DIR, EXIFTOOL_EXECUTABLE)
EXIFTOOL_FILES_DIR = os.path.join(BASE_DIR, "exiftool_files")
SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
IMAGE_PREVIEW_SIZE = (700, 500)
CUSTOMTK_IMAGE_PREVIEW_SIZE = (1400, 1000)
