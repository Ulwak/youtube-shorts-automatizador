import sqlite3
import logging
from datetime import datetime
from pathlib import Path

log_db = logging.getLogger("database")

def conectar_db(ruta_raiz):
    ruta_db = ruta_raiz / "database" / "registro.db"
    conectado = sqlite3.connect(ruta_db)
    guia = conectado.cursor()
    return guia, conectado

def desconectar_db(conectado):
    conectado.close()

def iniciar_db(ruta_raiz):
    ruta_sql = ruta_raiz / "database" / "registro.sql"
    
    guia = conectar_db(ruta_raiz)

    with open(ruta_sql, "r") as sql:
        codigo_sql = sql.read()

    guia[0].executescript(codigo_sql)
    
    guia[1].commit()
    desconectar_db(guia[1])

def verificar_si_hay_respaldos(ruta_raiz):
    guia = conectar_db(ruta_raiz)
    guia[0].execute("SELECT Fecha_Respaldo From respaldos ORDER BY ID DESC LIMIT 1")
    ultimo_respaldo = guia[0].fetchone()
    desconectar_db(guia[1])
    if ultimo_respaldo:
        return ultimo_respaldo[0]
    return None

def registrar_nuevo_respaldo(hora_respaldo, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:
        guia[0].execute("INSERT INTO respaldos (Fecha_Respaldo) VALUES (?)", (hora_respaldo, ))
        guia[1].commit()
    finally:
        desconectar_db(guia[1])

def realizar_respaldo(ruta_raiz):
    guia = conectar_db(ruta_raiz)
    carpeta_respaldo = ruta_raiz / "Respaldo-DB"
    carpeta_respaldo.mkdir(parents=True, exist_ok=True)
    destino_respaldo = carpeta_respaldo / "respaldo.db"
    destino = sqlite3.connect(destino_respaldo)
    try:
        with destino:
            guia[1].backup(destino)
    finally:
        desconectar_db(guia[1])
        desconectar_db(destino)

def respaldar(ruta_raiz):
    try:
        realizar_respaldo(ruta_raiz)
        fecha_respaldo = datetime.now().isoformat()
        registrar_nuevo_respaldo(fecha_respaldo, ruta_raiz)
        print("Respaldo de la Base de Datos creado")
        log_db.info("Respaldo de la Base de Datos creado")
    except Exception as error_db:
        log_db.exception(f"Ocurrio un error al realizar el respaldo de la base de datos: {error_db}")
        print(f"Ocurrio un error al momento de crear el respaldo, error detallado en el log 'Database'.")
    
def eliminador_registros_antiguos(tabla, eliminado, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:
        guia[0].execute(f"DELETE FROM {tabla} WHERE Nombre = ?", (eliminado,))
        guia[1].commit()
    finally:    
        desconectar_db(guia[1])

def actualizador_archivos_db(tabla, nombre, ruta, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:
        guia[0].execute(f"INSERT OR IGNORE INTO {tabla} (Nombre, Ruta) VALUES (?, ?)", (nombre, ruta,))
        guia[1].commit()
    finally:
        desconectar_db(guia[1])

def obtener_horarios_carpetas(tabla, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    guia[0].execute(f"SELECT Fecha_modificacion FROM revisiones WHERE Nombre = ?", (tabla,))
    fecha = guia[0].fetchone()
    desconectar_db(guia[1])
    return fecha

def registrador_revisiones(fecha, nombre, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:
        guia[0].execute("INSERT OR IGNORE INTO revisiones (Nombre, Fecha_modificacion) VALUES (?, ?)", (nombre, fecha,))
        guia[0].execute("UPDATE revisiones SET Fecha_modificacion = ? WHERE Nombre = ?", (fecha, nombre,))
        guia[1].commit()
    finally:
        desconectar_db(guia[1])

def obtener_todos_registros_db(tabla, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    guia[0].execute(f"SELECT Nombre FROM {tabla}")
    nombres = [nombre[0] for nombre in guia[0].fetchall()]
    desconectar_db(guia[1])
    return nombres

def obtener_memes(categoria, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    intentos = 0
    while intentos < 2:
        guia[0].execute("SELECT Ruta FROM memes WHERE Estado = 0 AND Categoria = ? ORDER BY RANDOM() LIMIT 2", (categoria,))
        rutas = [Path(ruta[0]) for ruta in guia[0].fetchall()]
        if len(rutas) == 2:
            desconectar_db(guia[1])
            return rutas
        elif intentos == 0:
            reciclar_memes(categoria, ruta_raiz)
            intentos += 1
        else:
            desconectar_db(guia[1])
            print(f"Rellene la carpeta de memes con minimo 2 memes en la categoria {categoria}")
            log_db.error(f"Hay menos de 2 imagenes en la carpeta de memes en la categoria {categoria}. Rellenar para continuar el funcionamiento normal.")
            exit()

def obtener_archivos(tipo, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    intentos = 0
    while intentos < 2:
        guia[0].execute(f"SELECT Ruta FROM {tipo} WHERE Estado = 0 ORDER BY RANDOM() LIMIT 1")
        archivo = guia[0].fetchone()
        if archivo:
            archivo = archivo[0]
            desconectar_db(guia[1])
            return Path(archivo)
        elif intentos == 0:
            reciclar_archivos(tipo, ruta_raiz)
            intentos += 1
        else:
            desconectar_db(guia[1])
            print(f"Rellene la carpeta de {tipo} con imagenes.")
            log_db.error(f"Faltan imagenes en la carpeta de {tipo}. Rellenar para continuar el funcionamiento normal.")
            exit()

def registrar_shorts(id_del_short, nombre, hora_subida, fecha_creacion, categoria, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:
        guia[0].execute("INSERT INTO shorts (Short_ID, Nombre, Hora_Subida, Fecha_Creacion, Categoria) VALUES (?, ?, ?, ?, ?)", (id_del_short, nombre, hora_subida, fecha_creacion, categoria,))
        guia[1].commit()
    finally:
        desconectar_db(guia[1])

def obtener_horario(ruta_raiz):
    guia = conectar_db(ruta_raiz)
    guia[0].execute("SELECT Hora_Subida FROM shorts ORDER BY Hora_Subida DESC LIMIT 1")
    horario = guia[0].fetchone()
    desconectar_db(guia[1])
    return horario
        
def actualizar_db(tabla, ruta, fecha, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:
        guia[0].execute(f"UPDATE {tabla} SET Estado = 1, Fecha_uso = ? WHERE Ruta = ?", (fecha, ruta,))
        guia[1].commit()
    finally:
        desconectar_db(guia[1])

def reciclar_archivos(tipo, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:    
        guia[0].execute(f"UPDATE {tipo} SET Estado = 0")
        guia[1].commit()
    finally:
        desconectar_db(guia[1])

def reciclar_memes(categoria, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:    
        guia[0].execute("UPDATE Memes SET Estado = 0 WHERE Categoria = ?", (categoria,))
        guia[1].commit()
    finally:    
        desconectar_db(guia[1])

def verificar_nombre(nombre_meme, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    guia[0].execute("SELECT 1 FROM Memes WHERE Nombre = ?", (nombre_meme,))
    existe = guia[0].fetchall()
    desconectar_db(guia[1])

    if existe:
        return False
    return True

def verificar_phash(hash_meme, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    guia[0].execute("SELECT 1 FROM Memes WHERE Phash = ?", (hash_meme,))
    existe = guia[0].fetchall()
    desconectar_db(guia[1])

    if existe:
        return False
    return True

def registrar(categoria, nombre_meme, hash_meme, Ruta, tiempo, ruta_raiz):
    guia = conectar_db(ruta_raiz)
    try:
        guia[0].execute("INSERT INTO Memes (Categoria, Nombre, Phash, Ruta, Fecha) VALUES (?, ?, ?, ?, ?)", (categoria, nombre_meme, hash_meme, Ruta, tiempo))
        guia[1].commit()
    finally:
        desconectar_db(guia[1])