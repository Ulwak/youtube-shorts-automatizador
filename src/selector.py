import random
from pathlib import Path

def seleccionar_archivo(ruta):
    archivo = Path(ruta)
    archivo_2 = [n for n in archivo.iterdir() if n.is_file()]
    return random.choice(archivo_2)

def mover_archivo(ruta, archivo):
    archivo.rename(Path(ruta / "usados" / archivo.name))

def seleccionar_categoria():
    contenido = Path(__file__).parent.parent / "memes" / "disponibles"
    carpeta = [n for n in contenido.iterdir() if n.is_dir()]
    return random.choice(carpeta)

def seleccionar_memes(carpeta):
    memes = [n for n in carpeta.iterdir() if n.is_file()]
    return random.sample(memes, 2)

def mover_memes_a_usados(memes):
    for meme in memes:
        categoria = meme.parent.name
        meme.rename(Path(__file__).parent.parent / "memes" / "usados" / categoria / meme.name)

def revisar_si_hay_memes_disponibles(carpeta, memes):
    if not memes:
            memes_usados = Path(__file__).parent.parent / "memes" / "usados" / carpeta.name
            usados = [n for n in memes_usados.iterdir() if n.is_file()]
            for usado in usados:
             usado.rename(Path(__file__).parent.parent / "memes" / "disponibles" / carpeta.name / usado.name)
            return seleccionar_memes(carpeta)

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
        memes = revisar_si_hay_memes_disponibles(carpeta, memes)
    mover_memes_a_usados(memes)
    mover_archivo(ruta_fondo, fondo)
    mover_archivo(ruta_like, like)
    mover_archivo(ruta_musica, musica)
    mover_archivo(ruta_comentarios, comentarios)
    return memes, fondo, like, musica, comentarios

if __name__ == "__main__":
    main()
