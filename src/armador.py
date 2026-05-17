from selector import seleccionador_archivos
from ensamblador import ensamblador_short

def main():
    for _ in range(4):
        memes, fondo, like, musica, comentarios = seleccionador_archivos()
        ensamblador_short(memes, fondo, like, musica, comentarios)

if __name__ == "__main__":
    main()