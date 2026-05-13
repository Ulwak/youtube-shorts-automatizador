import random
from pathlib import Path

def seleccionar_categoria():
    contenido = Path(__file__).parent.parent / "memes" / "disponibles"
    carpetas = [n for n in contenido.iterdir() if n.is_dir()]
    return random.choice(carpetas)