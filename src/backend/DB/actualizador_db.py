from datetime import datetime

def actualizar_archivos(tabla, actualizador_archivos_db, registrador_revisiones, obtener_todos_los_registros_db, eliminador_registros_antiguos, ruta_raiz):
    ruta = ruta_raiz / tabla
    archivo_2 = [n for n in ruta.iterdir() if n.is_file() and not n.name.startswith('.')]
    registros_disco_duro = {n.name for n in archivo_2}
    registros_db = set(obtener_todos_los_registros_db(tabla, ruta_raiz))
    eliminados = registros_db - registros_disco_duro
    for nombre in archivo_2:
        actualizador_archivos_db(tabla, nombre.name, str(nombre), ruta_raiz)
    for eliminado in eliminados:
        eliminador_registros_antiguos(tabla, eliminado, ruta_raiz)
    fecha = datetime.now().isoformat()
    registrador_revisiones(fecha, tabla, ruta_raiz)
    print(f"Actualizada {tabla}")
    
def verificar_ultima_fecha_modificacion(tabla, obtener_horarios_carpetas, ruta_raiz):
    fecha = obtener_horarios_carpetas(tabla, ruta_raiz)
    if fecha is None:
        return None
    fecha = fecha[0]
    return fecha

def comparar_fechas_de_modificacion(fecha_ultima_modificacion_registrada, tabla, ruta_raiz):
    ruta_carpeta = ruta_raiz / tabla
    ultima_modificacion = ruta_carpeta.stat().st_mtime
    fecha_modificacion = datetime.fromtimestamp(ultima_modificacion)
    fecha_ultima_modificacion_registrada = datetime.fromisoformat(fecha_ultima_modificacion_registrada)
    if fecha_modificacion > fecha_ultima_modificacion_registrada:
        return True
    return False
