import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess


class EtiquetadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Etiquetador de Imágenes")
        self.root.geometry("800x600")

        self.exiftool_path = os.path.join(
            os.path.dirname(__file__), "exiftool.exe")

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
            self.lista_imagenes = []
            for root_dir, _, files in os.walk(self.carpeta):
                for f in files:
                    if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                        self.lista_imagenes.append(os.path.join(root_dir, f))
            self.lista_imagenes.sort()

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

        # Mostrar imagen
        try:
            imagen = Image.open(ruta_imagen)
            imagen.thumbnail((700, 500))
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagen_label.config(image=imagen_tk)
            self.imagen_label.image = imagen_tk
        except Exception as e:
            messagebox.showerror("Error al mostrar imagen",
                                 f"No se pudo cargar la imagen:\n{e}")
            return

        # Leer etiquetas desde metadatos con exiftool
        try:
            resultado = subprocess.run(
                [self.exiftool_path, "-keywords", "-s3", ruta_imagen],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            etiquetas = resultado.stdout.strip().split(
                "\n") if resultado.stdout.strip() else []
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

        nombre_archivo = self.lista_imagenes[self.indice_actual]
        ruta_imagen = os.path.abspath(
            os.path.join(self.carpeta, nombre_archivo))
        etiquetas = [e.strip()
                     for e in self.etiquetas_entry.get().split(",") if e.strip()]

        try:
            # Construir argumentos para exiftool
            comando = [self.exiftool_path]
            comando += [f"-keywords={etiqueta}" for etiqueta in etiquetas]
            comando += ["-overwrite_original", ruta_imagen]

            subprocess.run(comando, check=True)
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


# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    app = EtiquetadorApp(root)
    root.mainloop()
