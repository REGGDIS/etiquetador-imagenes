import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import ImageTk

from app.services.image_service import buscar_imagenes, cargar_imagen
from app.services.metadata_service import MetadataError, leer_etiquetas, escribir_etiquetas
from app.services.tag_service import normalizar_etiquetas_desde_texto, normalizar_texto_etiqueta


class EtiquetadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Etiquetador de Imágenes")
        self.root.geometry("800x700")

        self.lista_imagenes = []
        self.lista_imagenes_filtrada = []
        self.busqueda_activa = False
        self.texto_busqueda_actual = ""
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

        busqueda_frame = tk.Frame(root)
        busqueda_frame.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(busqueda_frame, text="Buscar por etiqueta:").pack(anchor="w")

        busqueda_controles_frame = tk.Frame(busqueda_frame)
        busqueda_controles_frame.pack(fill="x", pady=(2, 0))

        self.busqueda_entry = tk.Entry(busqueda_controles_frame, width=50)
        self.busqueda_entry.pack(side="left", fill="x", expand=True)

        self.boton_buscar = tk.Button(
            busqueda_controles_frame, text="Buscar", command=self.buscar_por_etiqueta)
        self.boton_buscar.pack(side="left", padx=(10, 0))

        self.boton_limpiar_busqueda = tk.Button(
            busqueda_controles_frame, text="Limpiar búsqueda", command=self.limpiar_busqueda)
        self.boton_limpiar_busqueda.pack(side="left", padx=(10, 0))

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
            self.limpiar_estado_busqueda()

            if not self.lista_imagenes:
                self.indice_actual = 0
                self.limpiar_vista_imagen()
                self.actualizar_informacion()
                self.estado_var.set("Sin imágenes en la carpeta seleccionada.")
                self.actualizar_estado_botones()
                messagebox.showinfo(
                    "Sin imágenes", "No se encontraron imágenes válidas en la carpeta seleccionada.")
                return

            self.indice_actual = 0
            self.estado_var.set("Carpeta cargada correctamente.")
            self.mostrar_imagen()

    def obtener_lista_actual(self):
        if self.busqueda_activa:
            return self.lista_imagenes_filtrada
        return self.lista_imagenes

    def limpiar_estado_busqueda(self):
        self.lista_imagenes_filtrada = []
        self.busqueda_activa = False
        self.texto_busqueda_actual = ""
        self.busqueda_entry.delete(0, tk.END)

    def limpiar_vista_imagen(self):
        self.imagen_label.config(image="")
        self.imagen_label.image = None
        self.etiquetas_entry.delete(0, tk.END)
        self.root.title("Etiquetador de Imágenes")

    def buscar_por_etiqueta(self):
        if not self.lista_imagenes:
            return

        texto_busqueda = normalizar_texto_etiqueta(self.busqueda_entry.get())
        if not texto_busqueda:
            self.estado_var.set("Ingrese una etiqueta para buscar.")
            return

        resultados = []
        errores = 0

        for ruta_imagen in self.lista_imagenes:
            try:
                etiquetas = leer_etiquetas(os.path.abspath(ruta_imagen))
            except MetadataError:
                errores += 1
                continue

            texto_etiquetas = ", ".join(etiquetas)
            etiquetas_normalizadas = normalizar_etiquetas_desde_texto(
                texto_etiquetas)

            if texto_busqueda in etiquetas_normalizadas:
                resultados.append(ruta_imagen)

        self.lista_imagenes_filtrada = resultados
        self.busqueda_activa = True
        self.texto_busqueda_actual = texto_busqueda
        self.indice_actual = 0

        if resultados:
            self.mostrar_imagen()
            mensaje = (
                f"Búsqueda activa: {len(resultados)} resultado(s) "
                f"para \"{texto_busqueda}\"."
            )
        else:
            self.limpiar_vista_imagen()
            self.actualizar_informacion()
            self.actualizar_estado_botones()
            mensaje = f"Sin resultados para \"{texto_busqueda}\"."

        if errores:
            mensaje += f" {errores} imagen(es) no pudieron leerse."

        self.estado_var.set(mensaje)

    def limpiar_busqueda(self):
        self.limpiar_estado_busqueda()
        self.indice_actual = 0

        if self.lista_imagenes:
            self.estado_var.set("Búsqueda limpiada. Mostrando todas las imágenes.")
            self.mostrar_imagen()
        else:
            self.limpiar_vista_imagen()
            self.actualizar_informacion()
            self.estado_var.set("Seleccione una carpeta para comenzar.")
            self.actualizar_estado_botones()

    def mostrar_imagen(self):
        lista_actual = self.obtener_lista_actual()
        if not lista_actual:
            return

        ruta_imagen = os.path.abspath(lista_actual[self.indice_actual])
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
            f"{nombre_archivo} - {self.indice_actual + 1}/{len(lista_actual)}")

    def guardar_etiquetas(self):
        lista_actual = self.obtener_lista_actual()
        if not lista_actual:
            return

        ruta_imagen = os.path.abspath(lista_actual[self.indice_actual])
        etiquetas = normalizar_etiquetas_desde_texto(self.etiquetas_entry.get())

        try:
            escribir_etiquetas(ruta_imagen, etiquetas)
            self.etiquetas_entry.delete(0, tk.END)
            self.etiquetas_entry.insert(0, ", ".join(etiquetas))
            if self.busqueda_activa:
                self.estado_var.set(
                    "Etiquetas guardadas. Repite la búsqueda si quieres actualizar los resultados."
                )
            else:
                self.estado_var.set("Etiquetas guardadas correctamente.")
            messagebox.showinfo(
                "Guardado", "Etiquetas escritas en los metadatos del archivo.")
        except MetadataError as e:
            self.estado_var.set("No se pudieron guardar las etiquetas.")
            messagebox.showerror(
                "Error de ExifTool", str(e))

    def imagen_siguiente(self):
        lista_actual = self.obtener_lista_actual()
        if self.indice_actual < len(lista_actual) - 1:
            self.indice_actual += 1
            self.mostrar_imagen()

    def imagen_anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrar_imagen()

    def actualizar_informacion(self):
        lista_actual = self.obtener_lista_actual()
        if not lista_actual:
            self.nombre_imagen_var.set("Sin imagen cargada")
            self.contador_var.set("Imagen 0 de 0")
        else:
            ruta_imagen = os.path.abspath(lista_actual[self.indice_actual])
            self.nombre_imagen_var.set(os.path.basename(ruta_imagen))
            self.contador_var.set(
                f"Imagen {self.indice_actual + 1} de {len(lista_actual)}")

        if self.carpeta:
            self.carpeta_var.set(f"Carpeta: {self.carpeta}")
        else:
            self.carpeta_var.set("Carpeta: ninguna")

    def actualizar_estado_botones(self):
        lista_actual = self.obtener_lista_actual()
        hay_imagenes_visibles = bool(lista_actual)
        hay_imagenes_cargadas = bool(self.lista_imagenes)
        self.boton_guardar.config(
            state=tk.NORMAL if hay_imagenes_visibles else tk.DISABLED)
        self.boton_anterior.config(
            state=tk.NORMAL if hay_imagenes_visibles and self.indice_actual > 0 else tk.DISABLED)
        self.boton_siguiente.config(
            state=tk.NORMAL
            if hay_imagenes_visibles and self.indice_actual < len(lista_actual) - 1
            else tk.DISABLED)
        self.boton_buscar.config(
            state=tk.NORMAL if hay_imagenes_cargadas else tk.DISABLED)
        self.boton_limpiar_busqueda.config(
            state=tk.NORMAL if self.busqueda_activa else tk.DISABLED)
