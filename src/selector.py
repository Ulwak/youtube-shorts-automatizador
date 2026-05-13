import random
from pathlib import Path

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
    carpeta = seleccionar_categoria()
    try:
        memes = seleccionar_memes(carpeta)
    except:
       memes = revisar_si_hay_memes_disponibles(carpeta, memes)
    mover_memes_a_usados(memes)

if __name__ == "__main__":
    main()
