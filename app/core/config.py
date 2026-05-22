import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXIFTOOL_EXECUTABLE = "exiftool.exe"
EXIFTOOL_PATH = os.path.join(BASE_DIR, EXIFTOOL_EXECUTABLE)
SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
IMAGE_PREVIEW_SIZE = (700, 500)
