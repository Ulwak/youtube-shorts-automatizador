from selector import seleccionador_archivos, mover_archivo, mover_memes_a_usados
from ensamblador import ensamblador_short

def main():
    while True:
        try:
            i = int(input("Ingrese un numero mayor o igual a 1: "))
            if i >= 1:
                break
        except (ValueError):
            print("Ingrese un numero entero para continuar")
    for _ in range(i):
        memes, fondo, like, musica, comentarios, ruta_musica, ruta_fondo, ruta_like, ruta_comentarios = seleccionador_archivos()
        ensamblador_short(memes, fondo, like, musica, comentarios)
        mover_memes_a_usados(memes)
        mover_archivo(ruta_fondo, fondo)
        mover_archivo(ruta_like, like)
        mover_archivo(ruta_musica, musica)
        mover_archivo(ruta_comentarios, comentarios)

if __name__ == "__main__":
    main()