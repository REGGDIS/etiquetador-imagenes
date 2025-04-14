import os
import json
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

# Ruta del archivo JSON donde se guardarán las etiquetas
ETIQUETAS_FILE = "etiquetas.json"

# Cargar etiquetas si existen
if os.path.exists(ETIQUETAS_FILE):
    try:
        with open(ETIQUETAS_FILE, "r", encoding="utf-8") as f:
            etiquetas_dict = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Advertencia: el archivo etiquetas.json estaba vacío o mal formado. Se ignorará y se creará uno nuevo.")


class EtiquetadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Etiquetador de Imágenes")
        self.root.geometry("800x600")

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
            self.lista_imagenes = [
                f for f in os.listdir(self.carpeta)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
            ]
            self.lista_imagenes.sort()
            self.indice_actual = 0
            self.mostrar_imagen()

    def mostrar_imagen(self):
        if not self.lista_imagenes:
            return

        ruta_imagen = os.path.join(
            self.carpeta, self.lista_imagenes[self.indice_actual])
        imagen = Image.open(ruta_imagen)
        imagen.thumbnail((700, 500))
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_label.config(image=imagen_tk)
        self.imagen_label.image = imagen_tk

        # Mostrar etiquetas existentes
        nombre_archivo = self.lista_imagenes[self.indice_actual]
        etiquetas = etiquetas_dict.get(nombre_archivo, [])
        self.etiquetas_entry.delete(0, tk.END)
        self.etiquetas_entry.insert(0, ", ".join(etiquetas))

        self.root.title(
            f"{nombre_archivo} - {self.indice_actual + 1}/{len(self.lista_imagenes)}")

    def guardar_etiquetas(self):
        if not self.lista_imagenes:
            return
        nombre_archivo = self.lista_imagenes[self.indice_actual]
        etiquetas = [e.strip()
                     for e in self.etiquetas_entry.get().split(",") if e.strip()]
        etiquetas_dict[nombre_archivo] = etiquetas
        with open(ETIQUETAS_FILE, "w", encoding="utf-8") as f:
            json.dump(etiquetas_dict, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("Guardado", "Etiquetas guardadas con éxito.")

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
