import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import ImageTk

from app.services.image_service import buscar_imagenes, cargar_imagen
from app.services.metadata_service import MetadataError, leer_etiquetas, escribir_etiquetas
from app.services.tag_service import normalizar_etiquetas_desde_texto


class EtiquetadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Etiquetador de Imágenes")
        self.root.geometry("800x700")

        self.lista_imagenes = []
        self.indice_actual = 0
        self.carpeta = ""
        self.imagen_max_size = (760, 330)

        self.nombre_imagen_var = tk.StringVar(value="Sin imagen cargada")
        self.contador_var = tk.StringVar(value="Imagen 0 de 0")
        self.carpeta_var = tk.StringVar(value="Carpeta: ninguna")
        self.estado_var = tk.StringVar(value="Seleccione una carpeta para comenzar.")

        acciones_frame = tk.Frame(root)
        acciones_frame.pack(fill="x", padx=10, pady=10)

        self.boton_abrir_carpeta = tk.Button(
            acciones_frame, text="Abrir carpeta", command=self.abrir_carpeta)
        self.boton_abrir_carpeta.pack(side="left")

        info_frame = tk.Frame(root)
        info_frame.pack(fill="x", padx=10)

        tk.Label(info_frame, textvariable=self.nombre_imagen_var,
                 anchor="w").pack(fill="x")
        tk.Label(info_frame, textvariable=self.contador_var,
                 anchor="w").pack(fill="x")
        tk.Label(info_frame, textvariable=self.carpeta_var,
                 anchor="w").pack(fill="x")

        imagen_frame = tk.Frame(root, width=760, height=340)
        imagen_frame.pack(fill="both", expand=True, padx=10, pady=10)
        imagen_frame.pack_propagate(False)

        self.imagen_label = tk.Label(imagen_frame)
        self.imagen_label.pack(expand=True)

        controles_frame = tk.Frame(root)
        controles_frame.pack(fill="x", padx=10, pady=5)

        etiquetas_frame = tk.Frame(controles_frame)
        etiquetas_frame.pack(fill="x", pady=5)

        tk.Label(etiquetas_frame, text="Etiquetas:").pack(anchor="w")
        self.etiquetas_entry = tk.Entry(etiquetas_frame, width=50)
        self.etiquetas_entry.pack(fill="x")

        aviso = (
            "Recomendación: escribe etiquetas sin tildes ni caracteres especiales "
            "para mejorar la compatibilidad con el Explorador de Windows. "
            "Ejemplo: usar 'expedicion' en vez de 'expedición', 'guia' en vez de 'guía'."
        )
        tk.Label(etiquetas_frame, text=aviso, fg="gray", wraplength=760,
                 justify="left").pack(anchor="w", pady=(4, 0))

        botones_frame = tk.Frame(controles_frame)
        botones_frame.pack(fill="x", pady=5)

        self.boton_guardar = tk.Button(
            botones_frame, text="Guardar etiquetas", command=self.guardar_etiquetas)
        self.boton_guardar.pack(side="left")

        self.boton_anterior = tk.Button(
            botones_frame, text="Anterior", command=self.imagen_anterior)
        self.boton_anterior.pack(side="left", padx=10, pady=10)

        self.boton_siguiente = tk.Button(
            botones_frame, text="Siguiente", command=self.imagen_siguiente)
        self.boton_siguiente.pack(side="left", pady=10)

        estado_frame = tk.Frame(root)
        estado_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(estado_frame, textvariable=self.estado_var,
                 anchor="w", fg="gray").pack(fill="x")

        self.actualizar_estado_botones()

    def abrir_carpeta(self):
        self.carpeta = filedialog.askdirectory()
        if self.carpeta:
            self.lista_imagenes = buscar_imagenes(self.carpeta)

            if not self.lista_imagenes:
                self.indice_actual = 0
                self.imagen_label.config(image="")
                self.imagen_label.image = None
                self.etiquetas_entry.delete(0, tk.END)
                self.actualizar_informacion()
                self.estado_var.set("Sin imágenes en la carpeta seleccionada.")
                self.actualizar_estado_botones()
                messagebox.showinfo(
                    "Sin imágenes", "No se encontraron imágenes válidas en la carpeta seleccionada.")
                return

            self.indice_actual = 0
            self.estado_var.set("Carpeta cargada correctamente.")
            self.mostrar_imagen()

    def mostrar_imagen(self):
        if not self.lista_imagenes:
            return

        ruta_imagen = os.path.abspath(self.lista_imagenes[self.indice_actual])
        nombre_archivo = os.path.basename(ruta_imagen)
        self.actualizar_informacion()
        self.actualizar_estado_botones()

        try:
            imagen = cargar_imagen(ruta_imagen)
            imagen.thumbnail(self.imagen_max_size)
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagen_label.config(image=imagen_tk)
            self.imagen_label.image = imagen_tk
        except Exception as e:
            self.etiquetas_entry.delete(0, tk.END)
            self.estado_var.set("No se pudo cargar la imagen actual.")
            messagebox.showerror("Error al mostrar imagen",
                                 f"No se pudo cargar la imagen:\n{e}")
            return

        try:
            etiquetas = leer_etiquetas(ruta_imagen)
            self.etiquetas_entry.delete(0, tk.END)
            self.etiquetas_entry.insert(0, ", ".join(etiquetas))
        except MetadataError as e:
            messagebox.showerror("Error de ExifTool", str(e))
            self.etiquetas_entry.delete(0, tk.END)
            self.estado_var.set("No se pudieron leer las etiquetas.")

        self.root.title(
            f"{nombre_archivo} - {self.indice_actual + 1}/{len(self.lista_imagenes)}")

    def guardar_etiquetas(self):
        if not self.lista_imagenes:
            return

        ruta_imagen = os.path.abspath(self.lista_imagenes[self.indice_actual])
        etiquetas = normalizar_etiquetas_desde_texto(self.etiquetas_entry.get())

        try:
            escribir_etiquetas(ruta_imagen, etiquetas)
            self.etiquetas_entry.delete(0, tk.END)
            self.etiquetas_entry.insert(0, ", ".join(etiquetas))
            self.estado_var.set("Etiquetas guardadas correctamente.")
            messagebox.showinfo(
                "Guardado", "Etiquetas escritas en los metadatos del archivo.")
        except MetadataError as e:
            self.estado_var.set("No se pudieron guardar las etiquetas.")
            messagebox.showerror(
                "Error de ExifTool", str(e))

    def imagen_siguiente(self):
        if self.indice_actual < len(self.lista_imagenes) - 1:
            self.indice_actual += 1
            self.mostrar_imagen()

    def imagen_anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrar_imagen()

    def actualizar_informacion(self):
        if not self.lista_imagenes:
            self.nombre_imagen_var.set("Sin imagen cargada")
            self.contador_var.set("Imagen 0 de 0")
        else:
            ruta_imagen = os.path.abspath(self.lista_imagenes[self.indice_actual])
            self.nombre_imagen_var.set(os.path.basename(ruta_imagen))
            self.contador_var.set(
                f"Imagen {self.indice_actual + 1} de {len(self.lista_imagenes)}")

        if self.carpeta:
            self.carpeta_var.set(f"Carpeta: {self.carpeta}")
        else:
            self.carpeta_var.set("Carpeta: ninguna")

    def actualizar_estado_botones(self):
        hay_imagenes = bool(self.lista_imagenes)
        self.boton_guardar.config(
            state=tk.NORMAL if hay_imagenes else tk.DISABLED)
        self.boton_anterior.config(
            state=tk.NORMAL if hay_imagenes and self.indice_actual > 0 else tk.DISABLED)
        self.boton_siguiente.config(
            state=tk.NORMAL
            if hay_imagenes and self.indice_actual < len(self.lista_imagenes) - 1
            else tk.DISABLED)
