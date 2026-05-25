import os
from tkinter import filedialog, messagebox

import customtkinter as ctk

from app.services.image_service import buscar_imagenes, cargar_imagen
from app.services.metadata_service import MetadataError, leer_etiquetas, escribir_etiquetas
from app.services.tag_service import normalizar_etiquetas_desde_texto, normalizar_texto_etiqueta


class EtiquetadorCustomTkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Etiquetador de Imágenes - CustomTkinter POC")
        self.geometry("1180x760")
        self.minsize(980, 660)

        self.lista_imagenes = []
        self.lista_imagenes_filtrada = []
        self.busqueda_activa = False
        self.texto_busqueda_actual = ""
        self.indice_actual = 0
        self.carpeta = ""
        self.imagen_min_size = (620, 520)
        self.imagen_ctk = None
        self.redimensionar_imagen_id = None

        self.nombre_imagen_var = ctk.StringVar(value="Sin imagen cargada")
        self.contador_var = ctk.StringVar(value="Imagen 0 de 0")
        self.carpeta_var = ctk.StringVar(value="Carpeta: ninguna")
        self.estado_var = ctk.StringVar(value="Seleccione una carpeta para comenzar.")

        self._crear_interfaz()
        self.actualizar_estado_botones()

    def _crear_interfaz(self):
        self.grid_columnconfigure(0, weight=5, minsize=self.imagen_min_size[0])
        self.grid_columnconfigure(1, weight=0, minsize=330)
        self.grid_rowconfigure(0, weight=1)

        self.imagen_frame = ctk.CTkFrame(self, corner_radius=14)
        self.imagen_frame.grid(row=0, column=0, sticky="nsew", padx=(18, 10), pady=18)
        self.imagen_frame.grid_columnconfigure(0, weight=1)
        self.imagen_frame.grid_rowconfigure(0, weight=1)
        self.imagen_frame.bind("<Configure>", self._programar_redimension_imagen)

        self.imagen_label = None
        self._crear_imagen_label("Abra una carpeta para visualizar imágenes")

        controles_frame = ctk.CTkFrame(self, corner_radius=14, width=330)
        controles_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 18), pady=18)
        controles_frame.grid_columnconfigure(0, weight=1)
        controles_frame.grid_rowconfigure(6, weight=1)
        controles_frame.grid_propagate(False)

        encabezado_frame = ctk.CTkFrame(controles_frame, fg_color="transparent")
        encabezado_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 10))
        encabezado_frame.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            encabezado_frame,
            text="Etiquetador de Imágenes",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        titulo.grid(row=0, column=0, sticky="ew")

        subtitulo = ctk.CTkLabel(
            encabezado_frame,
            text="Prueba de concepto visual con CustomTkinter",
            text_color=("gray35", "gray72"),
            anchor="w",
            wraplength=290,
        )
        subtitulo.grid(row=1, column=0, sticky="ew", pady=(2, 10))

        self.boton_abrir_carpeta = ctk.CTkButton(
            encabezado_frame,
            text="Abrir carpeta",
            command=self.abrir_carpeta,
            height=38,
        )
        self.boton_abrir_carpeta.grid(row=2, column=0, sticky="ew")

        info_frame = ctk.CTkFrame(controles_frame, corner_radius=12)
        info_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))
        info_frame.grid_columnconfigure(0, weight=1)

        self.nombre_label = ctk.CTkLabel(
            info_frame,
            textvariable=self.nombre_imagen_var,
            anchor="w",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.nombre_label.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 2))

        self.contador_label = ctk.CTkLabel(
            info_frame,
            textvariable=self.contador_var,
            anchor="w",
            text_color=("gray30", "gray78"),
        )
        self.contador_label.grid(row=1, column=0, sticky="ew", padx=12, pady=2)

        self.carpeta_label = ctk.CTkLabel(
            info_frame,
            textvariable=self.carpeta_var,
            anchor="w",
            text_color=("gray30", "gray78"),
            wraplength=280,
        )
        self.carpeta_label.grid(row=2, column=0, sticky="ew", padx=12, pady=(2, 12))

        busqueda_frame = ctk.CTkFrame(controles_frame, fg_color="transparent")
        busqueda_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 10))
        busqueda_frame.grid_columnconfigure(0, weight=1)

        busqueda_label = ctk.CTkLabel(busqueda_frame, text="Buscar por etiqueta exacta")
        busqueda_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.busqueda_entry = ctk.CTkEntry(
            busqueda_frame,
            placeholder_text="Ejemplo: expedicion",
            height=36,
        )
        self.busqueda_entry.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.boton_buscar = ctk.CTkButton(
            busqueda_frame,
            text="Buscar",
            command=self.buscar_por_etiqueta,
            width=0,
            height=36,
        )
        self.boton_buscar.grid(row=2, column=0, sticky="ew", pady=(8, 0), padx=(0, 5))

        self.boton_limpiar_busqueda = ctk.CTkButton(
            busqueda_frame,
            text="Limpiar",
            command=self.limpiar_busqueda,
            width=0,
            height=36,
            fg_color=("gray58", "gray34"),
            hover_color=("gray48", "gray28"),
        )
        self.boton_limpiar_busqueda.grid(row=2, column=1, sticky="ew", pady=(8, 0), padx=(5, 0))

        etiquetas_frame = ctk.CTkFrame(controles_frame, fg_color="transparent")
        etiquetas_frame.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 10))
        etiquetas_frame.grid_columnconfigure(0, weight=1)

        etiquetas_label = ctk.CTkLabel(etiquetas_frame, text="Etiquetas")
        etiquetas_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.etiquetas_entry = ctk.CTkEntry(
            etiquetas_frame,
            placeholder_text="Separar etiquetas con coma",
            height=38,
        )
        self.etiquetas_entry.grid(row=1, column=0, sticky="ew")

        self.boton_guardar = ctk.CTkButton(
            etiquetas_frame,
            text="Guardar etiquetas",
            command=self.guardar_etiquetas,
            width=0,
            height=38,
        )
        self.boton_guardar.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        navegacion_frame = ctk.CTkFrame(controles_frame, fg_color="transparent")
        navegacion_frame.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 10))
        navegacion_frame.grid_columnconfigure((0, 1), weight=1)

        self.boton_anterior = ctk.CTkButton(
            navegacion_frame,
            text="Anterior",
            command=self.imagen_anterior,
            width=0,
            height=36,
        )
        self.boton_anterior.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.boton_siguiente = ctk.CTkButton(
            navegacion_frame,
            text="Siguiente",
            command=self.imagen_siguiente,
            width=0,
            height=36,
        )
        self.boton_siguiente.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        aviso = (
            "Recomendación: escribe etiquetas sin tildes ni caracteres especiales "
            "para mejorar la compatibilidad con el Explorador de Windows. "
            "Ejemplo: usar 'expedicion' en vez de 'expedición', 'guia' en vez de 'guía'."
        )
        aviso_label = ctk.CTkLabel(
            controles_frame,
            text=aviso,
            text_color=("gray38", "gray68"),
            anchor="w",
            justify="left",
            wraplength=290,
        )
        aviso_label.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 10))

        self.estado_label = ctk.CTkLabel(
            controles_frame,
            textvariable=self.estado_var,
            text_color=("gray28", "gray76"),
            anchor="sw",
            justify="left",
            wraplength=290,
        )
        self.estado_label.grid(row=7, column=0, sticky="ew", padx=16, pady=(0, 16))

    def _crear_imagen_label(self, texto):
        if self.imagen_label is not None:
            self.imagen_label.destroy()

        self.imagen_label = ctk.CTkLabel(
            self.imagen_frame,
            text=texto,
            fg_color=("gray88", "gray16"),
            corner_radius=12,
            anchor="center",
        )
        self.imagen_label.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)

    def _programar_redimension_imagen(self, _event=None):
        if not self.obtener_lista_actual():
            return

        if self.redimensionar_imagen_id is not None:
            self.after_cancel(self.redimensionar_imagen_id)

        self.redimensionar_imagen_id = self.after(140, self._redimensionar_imagen_actual)

    def _redimensionar_imagen_actual(self):
        self.redimensionar_imagen_id = None
        lista_actual = self.obtener_lista_actual()
        if not lista_actual:
            return

        try:
            ruta_imagen = os.path.abspath(lista_actual[self.indice_actual])
            imagen = cargar_imagen(ruta_imagen)
            ancho, alto = self.calcular_tamano_imagen(imagen)
            self.imagen_ctk = ctk.CTkImage(
                light_image=imagen,
                dark_image=imagen,
                size=(ancho, alto),
            )
            self.imagen_label.configure(image=self.imagen_ctk, text="")
        except Exception:
            self.limpiar_vista_imagen()
            self.estado_var.set("No se pudo ajustar la imagen actual.")

    def abrir_carpeta(self):
        carpeta = filedialog.askdirectory()
        if not carpeta:
            return

        self.carpeta = carpeta
        self.lista_imagenes = buscar_imagenes(self.carpeta)
        self.limpiar_estado_busqueda()

        if not self.lista_imagenes:
            self.indice_actual = 0
            self.limpiar_vista_imagen()
            self.actualizar_informacion()
            self.estado_var.set("Sin imágenes en la carpeta seleccionada.")
            self.actualizar_estado_botones()
            messagebox.showinfo(
                "Sin imágenes",
                "No se encontraron imágenes válidas en la carpeta seleccionada.",
            )
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
        self.busqueda_entry.delete(0, "end")

    def limpiar_vista_imagen(self):
        self.imagen_ctk = None
        self._crear_imagen_label("Abra una carpeta para visualizar imágenes")
        self.etiquetas_entry.delete(0, "end")
        self.title("Etiquetador de Imágenes - CustomTkinter POC")

    def calcular_tamano_imagen(self, imagen):
        max_width, max_height = self.obtener_area_imagen_disponible()
        ancho, alto = imagen.size
        escala = min(max_width / ancho, max_height / alto, 1)

        return max(1, int(ancho * escala)), max(1, int(alto * escala))

    def obtener_area_imagen_disponible(self):
        self.update_idletasks()

        max_width = self.imagen_frame.winfo_width() - 52
        max_height = self.imagen_frame.winfo_height() - 52

        if max_width <= 1 or max_height <= 1:
            return self.imagen_min_size

        return max_width, max_height

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
            etiquetas_normalizadas = normalizar_etiquetas_desde_texto(texto_etiquetas)

            if texto_busqueda in etiquetas_normalizadas:
                resultados.append(ruta_imagen)

        self.lista_imagenes_filtrada = resultados
        self.busqueda_activa = True
        self.texto_busqueda_actual = texto_busqueda
        self.indice_actual = 0

        if resultados:
            self.mostrar_imagen()
            mensaje = f"Búsqueda activa: {len(resultados)} resultado(s) para \"{texto_busqueda}\"."
        else:
            self.limpiar_vista_imagen()
            self.imagen_label.configure(text="Sin resultados para la etiqueta buscada")
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
            self.limpiar_vista_imagen()
            self.actualizar_informacion()
            self.actualizar_estado_botones()
            return

        ruta_imagen = os.path.abspath(lista_actual[self.indice_actual])
        nombre_archivo = os.path.basename(ruta_imagen)
        self.actualizar_informacion()
        self.actualizar_estado_botones()

        try:
            imagen = cargar_imagen(ruta_imagen)
            ancho, alto = self.calcular_tamano_imagen(imagen)
            self.imagen_ctk = ctk.CTkImage(
                light_image=imagen,
                dark_image=imagen,
                size=(ancho, alto),
            )
            self.imagen_label.configure(image=self.imagen_ctk, text="")
        except Exception as error:
            self.etiquetas_entry.delete(0, "end")
            self.estado_var.set("No se pudo cargar la imagen actual.")
            messagebox.showerror(
                "Error al mostrar imagen",
                f"No se pudo cargar la imagen:\n{error}",
            )
            return

        try:
            etiquetas = leer_etiquetas(ruta_imagen)
            self.etiquetas_entry.delete(0, "end")
            self.etiquetas_entry.insert(0, ", ".join(etiquetas))
        except MetadataError as error:
            messagebox.showerror("Error de ExifTool", str(error))
            self.etiquetas_entry.delete(0, "end")
            self.estado_var.set("No se pudieron leer las etiquetas.")

        self.title(f"{nombre_archivo} - {self.indice_actual + 1}/{len(lista_actual)}")

    def guardar_etiquetas(self):
        lista_actual = self.obtener_lista_actual()
        if not lista_actual:
            return

        ruta_imagen = os.path.abspath(lista_actual[self.indice_actual])
        etiquetas = normalizar_etiquetas_desde_texto(self.etiquetas_entry.get())

        try:
            escribir_etiquetas(ruta_imagen, etiquetas)
            self.etiquetas_entry.delete(0, "end")
            self.etiquetas_entry.insert(0, ", ".join(etiquetas))
            if self.busqueda_activa:
                self.estado_var.set(
                    "Etiquetas guardadas. Repite la búsqueda si quieres actualizar los resultados."
                )
            else:
                self.estado_var.set("Etiquetas guardadas correctamente.")
            messagebox.showinfo(
                "Guardado",
                "Etiquetas escritas en los metadatos del archivo.",
            )
        except MetadataError as error:
            self.estado_var.set("No se pudieron guardar las etiquetas.")
            messagebox.showerror("Error de ExifTool", str(error))

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
            self.contador_var.set(f"Imagen {self.indice_actual + 1} de {len(lista_actual)}")

        if self.carpeta:
            self.carpeta_var.set(f"Carpeta: {self.carpeta}")
        else:
            self.carpeta_var.set("Carpeta: ninguna")

    def actualizar_estado_botones(self):
        lista_actual = self.obtener_lista_actual()
        hay_imagenes_visibles = bool(lista_actual)
        hay_imagenes_cargadas = bool(self.lista_imagenes)

        self.boton_guardar.configure(state="normal" if hay_imagenes_visibles else "disabled")
        self.boton_anterior.configure(
            state="normal"
            if hay_imagenes_visibles and self.indice_actual > 0
            else "disabled"
        )
        self.boton_siguiente.configure(
            state="normal"
            if hay_imagenes_visibles and self.indice_actual < len(lista_actual) - 1
            else "disabled"
        )
        self.boton_buscar.configure(state="normal" if hay_imagenes_cargadas else "disabled")
        self.boton_limpiar_busqueda.configure(state="normal" if self.busqueda_activa else "disabled")
