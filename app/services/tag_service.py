_REEMPLAZOS_TILDES = str.maketrans({
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ü": "u",
})


def quitar_tildes(texto: str) -> str:
    return texto.translate(_REEMPLAZOS_TILDES)


def normalizar_texto_etiqueta(texto: str) -> str:
    return quitar_tildes(texto.strip().lower())


def eliminar_duplicados(etiquetas: list[str]) -> list[str]:
    etiquetas_unicas = []
    vistas = set()

    for etiqueta in etiquetas:
        if etiqueta not in vistas:
            etiquetas_unicas.append(etiqueta)
            vistas.add(etiqueta)

    return etiquetas_unicas


def normalizar_etiquetas_desde_texto(texto: str) -> list[str]:
    etiquetas = [
        normalizar_texto_etiqueta(etiqueta)
        for etiqueta in texto.split(",")
    ]
    etiquetas = [etiqueta for etiqueta in etiquetas if etiqueta]

    return eliminar_duplicados(etiquetas)
