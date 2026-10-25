from time import perf_counter
tiempo_inicial = perf_counter()
import datetime
from pathlib import Path
from Base.selector import seleccionador_archivos
from Base.ensamblador import ensamblador_short
from DB.actualizador_db import actualizar_archivos, verificar_ultima_fecha_modificacion, comparar_fechas_de_modificacion
from api_memes_google.descargador_y_verificador_memes import descargador_verificador, obtener_memes_ya_almacenados
from DB.verificadores_creador_sql import iniciar_db, obtener_memes, obtener_archivos, actualizar_db, registrar_shorts, obtener_horario, obtener_horarios_carpetas, actualizador_archivos_db, registrador_revisiones, obtener_todos_registros_db, eliminador_registros_antiguos, verificar_si_hay_respaldos, respaldar
from Base.subidor import subir_short
from Base.log import crear_logs

def main():
    ruta_raiz = Path(__file__).parent.parent.parent
    logs = crear_logs(ruta_raiz)
    try:
        iniciar_db(ruta_raiz)
        logs["database"].info("Base de datos inicializada correctamente")
        logs["ejecucion"].info("Base de datos inicializada correctamente")
        respaldo = verificar_si_hay_respaldos(ruta_raiz)
        if respaldo is not None:
            ultimo_respaldo = datetime.datetime.fromisoformat(respaldo)
            fecha_actual = datetime.datetime.now()
            diferencia = (fecha_actual - ultimo_respaldo).days
            if diferencia >= 1:
                while True:
                    decision = input(f"Han pasado {diferencia} dias desde el ultimo respaldo de la base de datos, ¿Desea realizar un respaldo ahora? (Si / No): ").lower()
                    if decision not in ["si", "no"]:
                        print("Ingrese una opcion valida (Si / No)")
                    elif decision == "si":
                            respaldar(ruta_raiz)
                            break
                    else:
                        print("Omitiendo el respaldo por decision del usuario")
                        logs["database"].warning(f"El ultimo respaldo de la DB fue hace {diferencia} dias")
                        break
        else:
            while True:
                decision = input("No se encontraron respaldos de la Base de Datos, ¿Desea realizar un respaldo ahora? (Si / No): ").lower()
                if decision not in ["si", "no"]:
                    print("Ingrese una opcion valida (Si / No)")
                elif decision == "si":
                    respaldar(ruta_raiz)
                    break
                else:
                    print("Omitiendo el respaldo por peticion del usuario.")
                    logs["database"].warning("No existe un respaldo para la DB")
                    break
                
    except Exception as error_bd:
        logs["database"].exception(f"Ocurrio un error con la base de datos: {error_bd}")
        exit()

    tablas = ["musica", "comentarios", "fondos", "likes"]
    print("Actualizando datos de la DB")
    for tabla in tablas:
        ultima_modificacion = verificar_ultima_fecha_modificacion(tabla, obtener_horarios_carpetas, ruta_raiz)
        if ultima_modificacion is None:
            actualizar_archivos(tabla, actualizador_archivos_db, registrador_revisiones, obtener_todos_registros_db, eliminador_registros_antiguos, ruta_raiz)
        else:
            continuar = comparar_fechas_de_modificacion(ultima_modificacion, tabla, ruta_raiz)
            if continuar:
                actualizar_archivos(tabla, actualizador_archivos_db, registrador_revisiones, obtener_todos_registros_db, eliminador_registros_antiguos, ruta_raiz)
            
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
        descargador_verificador(cantidad_shorts, ruta_raiz)
        logs["ejecucion"].info("Descarga de memes realizada con exito")
    except Exception as error_red:
        logs["red"].exception(f"Ocurrio un error de red: {error_red}")
        stock = obtener_memes_ya_almacenados(ruta_raiz)
        if any(cantidad < (cantidad_shorts * 2) for cantidad in stock.values()):
            print("Se detecto que en las carpetas no hay la cantidad minima de memes. ¿Desea continuar? (Por cada short se utilizaran 2 memes, si una carpeta tiene menos que la cantidad de shorts * 2 el programa movera los memes usados correspondientes a esa categoria a la carpeta de disponibles para asegurar el funcionamiento aunque esto podria implicar la repeticion de memes.)")
            continuar = input("¿Desea continuar la ejecucion? (Ingrese 'Y' para continuar o ingrese cualquier letra / numero para detener la ejecucion y rellenar manualmente las carpetas con memes o ejecutar el programa nuevamente para intentar rellenar las carpetas mediante la API) ").lower()
            if continuar not in ["y", "yes", "si", "sí"]:
                logs["ejecucion"].info("Finaliza la ejecucion por fallo de red")
                exit()

    for _ in range(cantidad_shorts):
        memes, elementos, carpeta = seleccionador_archivos(obtener_memes, obtener_archivos, ruta_raiz)
        logs["ejecucion"].info("Se seleccionaron los memes para el short")
        ruta_short = ensamblador_short(memes, elementos[0], elementos[1], elementos[2], elementos[3], ruta_raiz)
        logs["ejecucion"].info("Se ensamblo el short")
        id_short = subir_short(ruta_short, carpeta.name, registrar_shorts, obtener_horario, ruta_raiz)
        logs["ejecucion"].info("Se subio el short")
        if id_short is None:
            print("No se movieron los archivos")
        else:
            fecha = datetime.date.today().isoformat()
            for elemento in elementos:
                actualizar_db(elemento.parent.name, str(elemento), fecha, ruta_raiz)
            for n in memes:
                actualizar_db(n.parent.parent.name, str(n), fecha, ruta_raiz)
            print(f"youtube.com/shorts/{id_short}")
            SHORTS_SUBIDOS = SHORTS_SUBIDOS + 1
            print(f"Shorts ya subidos: {SHORTS_SUBIDOS}")
    logs["ejecucion"].info("Finalizacion de la ejecucion del programa")
    tiempo_total = perf_counter() - tiempo_inicial
    logs["duracion"].info(f"Duracion total de la ejecucion: {tiempo_total}")
    return id_short

if __name__ == "__main__":
    main()