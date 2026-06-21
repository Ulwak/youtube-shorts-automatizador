import random
from pathlib import Path

#Esta funcion es reutilizable y permite mediante una ruta ya asignada determinar si hay archivos en la misma o en caso contrario reponerlos.
def verificar_y_seleccionar_archivos(ruta):
    try:
        archivo = (ruta / "disponibles")
        archivo_2 = [n for n in archivo.iterdir() if n.is_file() and not n.name.startswith('.')]
        return random.choice(archivo_2)
    except (ValueError, IndexError):
        ubicacion = (ruta / "usados")
        usados = [n for n in ubicacion.iterdir() if n.is_file() and not n.name.startswith('.')]
        for usado in usados:
            usado.rename(Path(ruta) / "disponibles" / usado.name)
        archivo_2 = [n for n in archivo.iterdir() if n.is_file() and not n.name.startswith('.')]
        if len(archivo_2) == 0:
            print(f"No quedan archivos en {ruta.name}, tanto la carpeta de disponibles como usados se encuentra vacia.")
            raise SystemExit("Rellene la carpeta con minimo un archivo.")
        return random.choice(archivo_2)

#Esta funcion mueve los archivos utilizando la ruta y su nombre para organizacion y futura reutilizacion
def mover_archivo(ruta, archivo):
    archivo.rename(ruta / "usados" / archivo.name)

#Esta funcion se encarga de seleccionar la categoria del short a crear en base a una lista de carpetas
def seleccionar_categoria():
    contenido = Path(__file__).parent.parent.parent / "memes" / "disponibles"
    carpeta = [n for n in contenido.iterdir() if n.is_dir()]
    return random.choice(carpeta)

#Encargada de poner los memes en el lugar de "usados" para evitar repetirlos y a futuro reutilizarlos
def mover_memes_a_usados(memes, ruta_raiz):
    for meme in memes:
        categoria = meme.parent.name
        meme.rename(ruta_raiz / "memes" / "usados" / categoria / meme.name)

#Se encarga de seleccionar los memes.En caso de que no haya memes en la carpeta de "disponibles" mueve los memes de "usados" a "disponibles" para seguir reutilizandolos
def seleccionar_y_verificar_memes(carpeta, ruta_raiz):
        memes = [n for n in carpeta.iterdir() if n.is_file() and not n.name.startswith('.')]
        if len(memes) >= 2:
            return random.sample(memes, 2)
        else:
            memes_usados = ruta_raiz / "memes" / "usados" / carpeta.name
            usados = [n for n in memes_usados.iterdir() if n.is_file() and not n.name.startswith('.')]
            for usado in usados:
                usado.rename(Path(__file__).parent.parent.parent / "memes" / "disponibles" / carpeta.name / usado.name)
            memes = [n for n in carpeta.iterdir() if n.is_file() and not n.name.startswith('.')]
            if len(memes) == 0 or len(memes) == 1:
                print(f"No quedan archivos en {carpeta.name}, tanto la carpeta de disponibles como usados se encuentra vacia.")
                raise SystemExit("Rellene la carpeta con minimo 2 memes.")
            return random.sample(memes, 2)

#Funcion principal encargada de ejecutar todo y otorgarle los archivos al script ensamblador.py
def seleccionador_archivos():
    ruta_raiz = Path(__file__).parent.parent.parent
    archivos = ["musica", "fondos", "likes", "comentarios"]
    rutas = []
    elementos = []
    for elemento in archivos:
        ruta_elemento = ruta_raiz / elemento
        archivo = verificar_y_seleccionar_archivos(ruta_elemento)
        rutas.append(ruta_elemento)
        elementos.append(archivo)
    carpeta = seleccionar_categoria()
    memes = seleccionar_y_verificar_memes(carpeta, ruta_raiz)

    return memes, elementos, rutas, carpeta, ruta_raiz