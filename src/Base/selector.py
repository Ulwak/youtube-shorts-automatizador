import random
import logging
from pathlib import Path

log_ejecucion = logging.getLogger("ejecucion")
log_selector = logging.getLogger("selector")

#Esta funcion se encarga de seleccionar la categoria del short a crear en base a una lista de carpetas
def seleccionar_categoria():
    contenido = Path(__file__).parent.parent.parent / "memes"
    carpeta = [n for n in contenido.iterdir() if n.is_dir()]
    return random.choice(carpeta)

#Funcion principal encargada de ejecutar todo y otorgarle los archivos al script ensamblador.py
def seleccionador_archivos(obtener_memes, obtener_archivos):
    archivos = ["musica", "fondos", "likes", "comentarios"]
    elementos = []
    for elemento in archivos:
        archivo = Path(obtener_archivos(elemento))
        elementos.append(archivo)
    categoria = seleccionar_categoria()
    memes = obtener_memes(categoria.name)
    
    return memes, elementos, categoria