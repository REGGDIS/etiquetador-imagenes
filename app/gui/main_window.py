import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import ImageTk

from app.services.image_service import buscar_imagenes, cargar_imagen
from app.services.metadata_service import leer_etiquetas, escribir_etiquetas


class EtiquetadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Etiquetador de Imágenes")
        self.root.geometry("800x700")

        self.imagen_label = tk.Label(root)
        self.imagen_label.pack()

        self.etiquetas_entry = tk.Entry(root, width=50)
        self.etiquetas_entry.pack(pady=10)

        self.boton_guardar = tk.Button(
            root, text="Guardar etiquetas", command=self.guardar_etiquetas)
        self.boton_guardar.pack()

        self.boton_anterior = tk.Button(
            root, text="Anterior", command=self.imagen_anterior)
        self.boton_anterior.pack(side="left", padx=10, pady=10)

        self.boton_siguiente = tk.Button(
            root, text="Siguiente", command=self.imagen_siguiente)
        self.boton_siguiente.pack(side="right", padx=10, pady=10)

        self.boton_abrir_carpeta = tk.Button(
            root, text="Abrir carpeta", command=self.abrir_carpeta)
        self.boton_abrir_carpeta.pack(pady=10)

        self.lista_imagenes = []
        self.indice_actual = 0
        self.carpeta = ""

    def abrir_carpeta(self):
        self.carpeta = filedialog.askdirectory()
        if self.carpeta:
            self.lista_imagenes = buscar_imagenes(self.carpeta)

            if not self.lista_imagenes:
                messagebox.showinfo(
                    "Sin imágenes", "No se encontraron imágenes válidas en la carpeta seleccionada.")
                return

            self.indice_actual = 0
            self.mostrar_imagen()

    def mostrar_imagen(self):
        if not self.lista_imagenes:
            return

        ruta_imagen = os.path.abspath(self.lista_imagenes[self.indice_actual])
        nombre_archivo = os.path.basename(ruta_imagen)

        try:
            imagen = cargar_imagen(ruta_imagen)
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagen_label.config(image=imagen_tk)
            self.imagen_label.image = imagen_tk
        except Exception as e:
            messagebox.showerror("Error al mostrar imagen",
                                 f"No se pudo cargar la imagen:\n{e}")
            return

        try:
            etiquetas = leer_etiquetas(ruta_imagen)
            self.etiquetas_entry.delete(0, tk.END)
            self.etiquetas_entry.insert(0, ", ".join(etiquetas))
        except Exception as e:
            print(f"No se pudieron leer las etiquetas con exiftool: {e}")
            self.etiquetas_entry.delete(0, tk.END)

        self.root.title(
            f"{nombre_archivo} - {self.indice_actual + 1}/{len(self.lista_imagenes)}")

    def guardar_etiquetas(self):
        if not self.lista_imagenes:
            return

        ruta_imagen = os.path.abspath(self.lista_imagenes[self.indice_actual])
        etiquetas = [e.strip()
                     for e in self.etiquetas_entry.get().split(",") if e.strip()]

        try:
            escribir_etiquetas(ruta_imagen, etiquetas)
            messagebox.showinfo(
                "Guardado", "Etiquetas escritas en los metadatos del archivo.")
        except Exception as e:
            print(f"Error al guardar etiquetas con exiftool: {e}")
            messagebox.showerror(
                "Error", f"No se pudo guardar con exiftool.\n{e}")

    def imagen_siguiente(self):
        if self.indice_actual < len(self.lista_imagenes) - 1:
            self.indice_actual += 1
            self.mostrar_imagen()

    def imagen_anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrar_imagen()
