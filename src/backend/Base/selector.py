import random
import logging

log_ejecucion = logging.getLogger("ejecucion")
log_selector = logging.getLogger("selector")

#Esta funcion se encarga de seleccionar la categoria del short a crear en base a una lista de carpetas
def seleccionar_categoria(ruta_raiz):
    contenido = ruta_raiz / "memes"
    carpeta = [n for n in contenido.iterdir() if n.is_dir()]
    return random.choice(carpeta)

#Funcion principal encargada de ejecutar todo y otorgarle los archivos al script ensamblador.py
def seleccionador_archivos(obtener_memes, obtener_archivos, ruta_raiz):
    archivos = ["musica", "fondos", "likes", "comentarios"]
    elementos = []
    for elemento in archivos:
        archivo = obtener_archivos(elemento, ruta_raiz)
        elementos.append(archivo)
    categoria = seleccionar_categoria(ruta_raiz)
    memes = obtener_memes(categoria.name, ruta_raiz)
    
    return memes, elementos, categoria