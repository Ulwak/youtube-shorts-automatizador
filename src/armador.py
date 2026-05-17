from selector import seleccionador_archivos, mover_archivo, mover_memes_a_usados
from ensamblador import ensamblador_short

def main():
    for _ in range(1):
        memes, fondo, like, musica, comentarios, ruta_musica, ruta_fondo, ruta_like, ruta_comentarios = seleccionador_archivos()
        ensamblador_short(memes, fondo, like, musica, comentarios)
        mover_memes_a_usados(memes)
        mover_archivo(ruta_fondo, fondo)
        mover_archivo(ruta_like, like)
        mover_archivo(ruta_musica, musica)
        mover_archivo(ruta_comentarios, comentarios)

if __name__ == "__main__":
    main()