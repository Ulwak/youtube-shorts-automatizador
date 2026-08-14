from time import perf_counter
tiempo_inicial = perf_counter()
from Base.selector import seleccionador_archivos, mover_archivo, mover_memes_a_usados
from Base.ensamblador import ensamblador_short
from api_memes_google.descargador_y_verificador_memes import descargador_verificador, obtener_memes_ya_almacenados
from api_memes_google.verificadores_creador_sql import iniciar_db
from Base.subidor import subir_short
from Base.log import crear_logs

def main():
    logs = crear_logs()
    try:
        iniciar_db()
        logs["database"].info("Base de datos inicializada correctamente")
        logs["ejecucion"].info("Base de datos inicializada correctamente")
    except Exception as error_bd:
        logs["database"].exception(f"Ocurrio un error con la base de datos: {error_bd}")
        exit()
    SHORTS_SUBIDOS = 0
    while True:
        try:
            cantidad_shorts = int(input("Ingrese la cantidad de shorts que usted desea crear (mayor o igual a 1): "))
            if cantidad_shorts >= 1:
                logs["ejecucion"].info(f"Cantidad de shorts requerida y validada (cantidad: {cantidad_shorts})")
                break
        except ValueError:
            print("Ingrese un numero entero para continuar")
            logs["inputs_usuario"].warning("El usuario ingreso un numero el cual no es entero")
    try:
        descargador_verificador(cantidad_shorts)
        logs["ejecucion"].info("Descarga de memes realizada con exito")
    except Exception as error_red:
        logs["red"].exception(f"Ocurrio un error de red: {error_red}")
        stock = obtener_memes_ya_almacenados()
        if any(cantidad < (cantidad_shorts * 2) for cantidad in stock.values()):
            print("Se detecto que en las carpetas no hay la cantidad minima de memes. ¿Desea continuar? (Por cada short se utilizaran 2 memes, si una carpeta tiene menos que la cantidad de shorts * 2 el programa movera los memes usados correspondientes a esa categoria a la carpeta de disponibles para asegurar el funcionamiento aunque esto podria implicar la repeticion de memes.)")
            continuar = input("¿Desea continuar la ejecucion? (Ingrese 'Y' para continuar o ingrese cualquier letra / numero para detener la ejecucion y rellenar manualmente las carpetas con memes o ejecutar el programa nuevamente para intentar rellenar las carpetas mediante la API) ")
            if continuar != "Y":
                logs["ejecucion"].info("Finaliza la ejecucion por fallo de red")
                exit()

    for _ in range(cantidad_shorts):
        memes, elementos, rutas, carpeta, ruta_raiz = seleccionador_archivos()
        logs["ejecucion"].info("Se seleccionaron los memes para el short")
        ruta_short = ensamblador_short(memes, elementos[1], elementos[2], elementos[0], elementos[3])
        logs["ejecucion"].info("Se ensamblo el short")
        id_short = subir_short(ruta_short, carpeta.name)
        logs["ejecucion"].info("Se subio el short")
        if id_short is None:
            print("No se movieron los archivos")
        else:
            for ruta, elemento in zip(rutas, elementos):
                mover_archivo(ruta, elemento)
            mover_memes_a_usados(memes, ruta_raiz)
            print(f"youtube.com/shorts/{id_short}")
            SHORTS_SUBIDOS = SHORTS_SUBIDOS + 1
            print(f"Shorts ya subidos: {SHORTS_SUBIDOS}")
    logs["ejecucion"].info("Finalizacion de la ejecucion del programa")
    tiempo_total = perf_counter() - tiempo_inicial
    logs["duracion"].info(f"Duracion total de la ejecucion: {tiempo_total}")

if __name__ == "__main__":
    main()