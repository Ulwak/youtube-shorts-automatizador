import random
from pathlib import Path

#Esta funcion es reutilizable y permite mediante una ruta ya asignada determinar si hay archivos en la misma o en caso contrario reponerlos.
def verificar_y_seleccionar_archivos(ruta):
    try:
        archivo = (ruta / "disponibles")
        archivo_2 = [n for n in archivo.iterdir() if n.is_file() and not n.name.startswith('.')]
        return random.choice(archivo_2)
    except ValueError:
        ubicacion = (ruta / "usados")
        usados = [n for n in ubicacion.iterdir() if n.is_file() and not n.name.startswith('.')]
        for usado in usados:
            usado.rename(Path(ruta) / "disponibles" / usado.name)
    return verificar_y_seleccionar_archivos(ruta)

#Esta funcion mueve los archivos utilizando la ruta y su nombre para organizacion y futura reutilizacion
def mover_archivo(ruta, archivo):
    archivo.rename(ruta / "usados" / archivo.name)

#Esta funcion se encarga de seleccionar la categoria del short a crear en base a una lista de carpetas
def seleccionar_categoria():
    contenido = Path(__file__).parent.parent / "memes" / "disponibles"
    carpeta = [n for n in contenido.iterdir() if n.is_dir()]
    return random.choice(carpeta)

#Encargada de poner los memes en el lugar de "usados" para evitar repetirlos y a futuro reutilizarlos
def mover_memes_a_usados(memes):
    for meme in memes:
        categoria = meme.parent.name
        meme.rename(Path(__file__).parent.parent / "memes" / "usados" / categoria / meme.name)

#Se encarga de seleccionar los memes.En caso de que no haya memes en la carpeta de "disponibles" mueve los memes de "usados" a "disponibles" para seguir reutilizandolos
def seleccionar_y_verificar_memes(carpeta):
    try:
        memes = [n for n in carpeta.iterdir() if n.is_file() and not n.name.startswith('.')]
        return random.sample(memes, 2)
    except ValueError:
        memes_usados = Path(__file__).parent.parent / "memes" / "usados" / carpeta.name
        usados = [n for n in memes_usados.iterdir() if n.is_file() and not n.name.startswith('.')]
        for usado in usados:
            usado.rename(Path(__file__).parent.parent / "memes" / "disponibles" / carpeta.name / usado.name)
    return seleccionar_y_verificar_memes(carpeta)

#Funcion principal encargada de ejecutar todo y otorgarle los archivos al script ensamblador.py
def seleccionador_archivos():
    ruta_musica = Path(__file__).parent.parent / "musica"
    ruta_fondo = Path(__file__).parent.parent / "fondos"
    ruta_like = Path(__file__).parent.parent / "likes"
    ruta_comentarios = Path(__file__).parent.parent / "comentarios"
    carpeta = seleccionar_categoria()
    fondo = verificar_y_seleccionar_archivos(ruta_fondo)
    like = verificar_y_seleccionar_archivos(ruta_like)
    musica = verificar_y_seleccionar_archivos(ruta_musica)
    comentarios = verificar_y_seleccionar_archivos(ruta_comentarios)
    memes = seleccionar_y_verificar_memes(carpeta)

    return memes, fondo, like, musica, comentarios, ruta_musica, ruta_fondo, ruta_like, ruta_comentarios