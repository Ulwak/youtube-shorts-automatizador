from selector import seleccionador_archivos, mover_archivo, mover_memes_a_usados
from ensamblador import ensamblador_short
from subidor import subir_short
from pathlib import Path

ruta_carpeta_memes_disponible = Path(__file__).parent.parent / "memes" / "disponibles"
categorias = [n for n in ruta_carpeta_memes_disponible.iterdir() if n.is_dir()]

def contar_memes(ruta_carpeta_memes_disponible, categorias):
    while True:
        try:
            memes_por_carpeta = int(input("Ingrese la cantidad de memes que tenia en sus carpetas antes de ejecutar el codigo (ejemplo 12): "))
            cantidad_minima_aviso = int(input("¿Cuando queres que se te avise que te estas quedando sin memes? (ejemplo 5 o 0 para desactivar): "))
            if memes_por_carpeta >= 1 and cantidad_minima_aviso >= 0:
                break
        except (ValueError):
            print("Ingrese un numero entero para continuar")
    if cantidad_minima_aviso == 0:
        print("El aviso esta desactivado por decision del usuario")
    for n in categorias:
        cantidad = len([f for f in (ruta_carpeta_memes_disponible / n.name).iterdir() if f.is_file() and not f.name.startswith('.')])
        memes_faltantes = max(0,memes_por_carpeta - cantidad)
        if cantidad <= cantidad_minima_aviso:
            print(f"Tenes menos de {cantidad_minima_aviso} memes en {n.name}")
        print(f"En {n.name} hay {cantidad} memes y se debe rellenar con {memes_faltantes}") 

def main():
    SHORTS_SUBIDOS = 0
    while True:
        try:
            i = int(input("Ingrese la cantidad de shorts que usted desea crear (mayor o igual a 1): "))
            if i >= 1:
                break
        except (ValueError):
            print("Ingrese un numero entero para continuar")
    for _ in range(i):
        memes, fondo, like, musica, comentarios, ruta_musica, ruta_fondo, ruta_like, ruta_comentarios, carpeta = seleccionador_archivos()
        ruta_short = ensamblador_short(memes, fondo, like, musica, comentarios)
        id_short = subir_short(ruta_short, carpeta.name)
        if id_short is None:
            print("No se movieron los archivos")
        else:
            mover_memes_a_usados(memes)
            mover_archivo(ruta_fondo, fondo)
            mover_archivo(ruta_like, like)
            mover_archivo(ruta_musica, musica)
            mover_archivo(ruta_comentarios, comentarios)
            print(f"youtube.com/shorts/{id_short}")
            SHORTS_SUBIDOS = SHORTS_SUBIDOS + 1
            print(f"Shorts ya subidos: {SHORTS_SUBIDOS}")
    contar_memes(ruta_carpeta_memes_disponible, categorias)

if __name__ == "__main__":
    main()