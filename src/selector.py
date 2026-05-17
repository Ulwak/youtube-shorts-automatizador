import random
from pathlib import Path

#Esta funcion es reutilizable ya que solo se le debe asignar la ruta de la carpeta logrando ahorrar varias lineas de codigo 
# y cumpliendo la misma funcion.
def seleccionar_archivo(ruta):
    archivo = Path(ruta)
    archivo_2 = [n for n in archivo.iterdir() if n.is_file() and not n.name.startswith('.')]
    return random.choice(archivo_2)

#Esta funcion mueve los archivos utilizando la ruta y su nombre para organizacion y futura reutilizacion
def mover_archivo(ruta, archivo):
    archivo.rename(Path(ruta / "usados" / archivo.name))

#Esta funcion se encarga de seleccionar la categoria del short a crear en base a una lista de carpetas
def seleccionar_categoria():
    contenido = Path(__file__).parent.parent / "memes" / "disponibles"
    carpeta = [n for n in contenido.iterdir() if n.is_dir()]
    return random.choice(carpeta)

#Encargada de seleccionar los memes a adjuntar en el video
def seleccionar_memes(carpeta):
    memes = [n for n in carpeta.iterdir() if n.is_file() and not n.name.startswith('.')]
    return random.sample(memes, 2)

#Encargada de poner los memes en el lugar de "usados" para evitar repetirlos y a futuro reutilizarlos
def mover_memes_a_usados(memes):
    for meme in memes:
        categoria = meme.parent.name
        meme.rename(Path(__file__).parent.parent / "memes" / "usados" / categoria / meme.name)

#Se encarga de que en caso de que no haya memes en la carpeta de "disponibles" se muevan los memes de "usados" a "disponibles" para seguir reutilizandolos
def revisar_si_hay_memes_disponibles(carpeta):
    memes_usados = Path(__file__).parent.parent / "memes" / "usados" / carpeta.name
    usados = [n for n in memes_usados.iterdir() if n.is_file() and not n.name.startswith('.')]
    for usado in usados:
        usado.rename(Path(__file__).parent.parent / "memes" / "disponibles" / carpeta.name / usado.name)
    return seleccionar_memes(carpeta)

#Funcion principal encargada de ejecutar todo y otorgarle los archivos al script ensamblador.py
def main():
    ruta_musica = Path(__file__).parent.parent / "musica"
    ruta_fondo = Path(__file__).parent.parent / "fondos"
    ruta_like = Path(__file__).parent.parent / "likes"
    ruta_comentarios = Path(__file__).parent.parent / "comentarios"
    carpeta = seleccionar_categoria()
    fondo = seleccionar_archivo(ruta_fondo / "disponibles")
    like = seleccionar_archivo(ruta_like / "disponibles")
    musica = seleccionar_archivo(ruta_musica / "disponibles")
    comentarios = seleccionar_archivo(ruta_comentarios / "disponibles")  
    try:
        memes = seleccionar_memes(carpeta)
    except:
        memes = revisar_si_hay_memes_disponibles(carpeta)
    mover_memes_a_usados(memes)
    mover_archivo(ruta_fondo, fondo)
    mover_archivo(ruta_like, like)
    mover_archivo(ruta_musica, musica)
    mover_archivo(ruta_comentarios, comentarios)
    
    return memes, fondo, like, musica, comentarios

if __name__ == "__main__":
    main()