from time import perf_counter
tiempo_inicial = perf_counter()
import datetime
from Base.selector import seleccionador_archivos
from Base.ensamblador import ensamblador_short
from api_memes_google.descargador_y_verificador_memes import descargador_verificador, obtener_memes_ya_almacenados
from api_memes_google.verificadores_creador_sql import iniciar_db, obtener_memes, obtener_archivos, actualizar_db, registrar_shorts, obtener_horario
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
            continuar = input("¿Desea continuar la ejecucion? (Ingrese 'Y' para continuar o ingrese cualquier letra / numero para detener la ejecucion y rellenar manualmente las carpetas con memes o ejecutar el programa nuevamente para intentar rellenar las carpetas mediante la API) ").lower()
            if continuar not in ["y", "yes", "si", "sí"]:
                logs["ejecucion"].info("Finaliza la ejecucion por fallo de red")
                exit()

    for _ in range(cantidad_shorts):
        memes, elementos, carpeta = seleccionador_archivos(obtener_memes, obtener_archivos)
        logs["ejecucion"].info("Se seleccionaron los memes para el short")
        ruta_short = ensamblador_short(memes, elementos[0], elementos[1], elementos[2], elementos[3])
        logs["ejecucion"].info("Se ensamblo el short")
        id_short = subir_short(ruta_short, carpeta.name, registrar_shorts, obtener_horario)
        logs["ejecucion"].info("Se subio el short")
        if id_short is None:
            print("No se movieron los archivos")
        else:
            fecha = datetime.date.today().isoformat()
            for elemento in elementos:
                actualizar_db(elemento.parent.name, str(elemento), fecha)
            for n in memes:
                actualizar_db(n.parent.parent.name, str(n), fecha)
            print(f"youtube.com/shorts/{id_short}")
            SHORTS_SUBIDOS = SHORTS_SUBIDOS + 1
            print(f"Shorts ya subidos: {SHORTS_SUBIDOS}")
    logs["ejecucion"].info("Finalizacion de la ejecucion del programa")
    tiempo_total = perf_counter() - tiempo_inicial
    logs["duracion"].info(f"Duracion total de la ejecucion: {tiempo_total}")

if __name__ == "__main__":
    main()