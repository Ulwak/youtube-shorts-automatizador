from Base.selector import seleccionador_archivos, mover_archivo, mover_memes_a_usados
from Base.ensamblador import ensamblador_short
from api_memes_google.descargador_y_verificador_memes import descargador_verificador, obtener_memes_ya_almacenados
from api_memes_google.verificadores_creador_sql import iniciar_db
from Base.subidor import subir_short
from pathlib import Path

def main():
    iniciar_db()
    SHORTS_SUBIDOS = 0
    while True:
        try:
            cantidad_shorts = int(input("Ingrese la cantidad de shorts que usted desea crear (mayor o igual a 1): "))
            if cantidad_shorts >= 1:
                break
        except ValueError:
            print("Ingrese un numero entero para continuar")
    try:
        descargador_verificador(cantidad_shorts)
    except Exception as Error:
        print(f"Error {Error}")
        stock = obtener_memes_ya_almacenados()
        if any(cantidad < (cantidad_shorts * 2) for cantidad in stock.values()):
            print("Se detecto que en las carpetas no hay la cantidad minima de memes. ¿Desea continuar? (Por cada short se utilizaran 2 memes, si una carpeta tiene menos que la cantidad de shorts * 2 el programa movera los memes usados correspondientes a esa categoria a la carpeta de disponibles para asegurar el funcionamiento aunque esto podria implicar la repeticion de memes.)")
            continuar = input("¿Desea continuar la ejecucion? (Ingrese 'Y' para continuar o ingrese cualquier letra / numero para detener la ejecucion y rellenar manualmente las carpetas con memes o ejecutar el programa nuevamente para intentar rellenar las carpetas mediante la API) ")
            if continuar != "Y":
                exit()
    for _ in range(cantidad_shorts):
        memes, elementos, rutas, carpeta, ruta_raiz = seleccionador_archivos()
        ruta_short = ensamblador_short(memes, elementos[1], elementos[2], elementos[0], elementos[3])
        id_short = subir_short(ruta_short, carpeta.name)
        if id_short is None:
            print("No se movieron los archivos")
        else:
            for ruta, elemento in zip(rutas, elementos):
                mover_archivo(ruta, elemento)
            mover_memes_a_usados(memes, ruta_raiz)
            print(f"youtube.com/shorts/{id_short}")
            SHORTS_SUBIDOS = SHORTS_SUBIDOS + 1
            print(f"Shorts ya subidos: {SHORTS_SUBIDOS}")

if __name__ == "__main__":
    main()