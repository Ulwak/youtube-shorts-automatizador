import sqlite3
import logging
from pathlib import Path

log_db = logging.getLogger("database")

ruta_db = Path(__file__).parent.parent.parent / "database" / "registro.db"

def conectar_db():
    conectado = sqlite3.connect(ruta_db)
    guia = conectado.cursor()
    return guia, conectado

def desconectar_db(conectado):
    conectado.close()

def iniciar_db():
    ruta_sql = Path(__file__).parent.parent.parent / "database" / "registro.sql"
    
    guia = conectar_db()

    with open(ruta_sql, "r") as sql:
        codigo_sql = sql.read()

    guia[0].executescript(codigo_sql)
    
    guia[1].commit()
    desconectar_db(guia[1])

def actualizador_datos_db_primera_vez(tabla, nombre, ruta):
    guia = conectar_db()
    guia[0].execute(f"INSERT INTO {tabla} (Nombre, Ruta) VALUES (?, ?)", (nombre, ruta,))
    guia[1].commit()
    print(f"Actualizado {nombre} en {tabla}")
    desconectar_db(guia[1])

def obtener_memes(categoria):
    guia = conectar_db()
    intentos = 0
    while intentos < 2:
        guia[0].execute("SELECT Ruta FROM memes WHERE Estado = 0 AND Categoria = ? ORDER BY RANDOM() LIMIT 2", (categoria,))
        rutas = [Path(ruta[0]) for ruta in guia[0].fetchall()]
        if len(rutas) == 2:
            desconectar_db(guia[1])
            return rutas
        elif intentos == 0:
            reciclar_memes(categoria)
            intentos += 1
        else:
            desconectar_db(guia[1])
            print(f"Rellene la carpeta de memes con minimo 2 memes en la categoria {categoria}")
            log_db.error(f"Hay menos de 2 imagenes en la carpeta de memes en la categoria {categoria}. Rellenar para continuar el funcionamiento normal.")
            exit()

def obtener_archivos(tipo):
    guia = conectar_db()
    intentos = 0
    while intentos < 2:
        guia[0].execute(f"SELECT Ruta FROM {tipo} WHERE Estado = 0 ORDER BY RANDOM() LIMIT 1")
        archivo = guia[0].fetchone()
        if archivo:
            archivo = archivo[0]
            desconectar_db(guia[1])
            return archivo
        elif intentos == 0:
            reciclar_archivos(tipo)
            intentos += 1
        else:
            desconectar_db(guia[1])
            print(f"Rellene la carpeta de {tipo} con minimo 2 memes.")
            log_db.error(f"Hay menos de 1 imagen en la carpeta de {tipo}. Rellenar para continuar el funcionamiento normal.")
            exit()

def registrar_shorts(id_del_short, nombre, hora_subida, fecha_creacion, categoria):
    guia = conectar_db()
    guia[0].execute("INSERT INTO shorts (Short_ID, Nombre, Hora_Subida, Fecha_Creacion, Categoria) VALUES (?, ?, ?, ?, ?)", (id_del_short, nombre, hora_subida, fecha_creacion, categoria,))
    guia[1].commit()
    desconectar_db(guia[1])

def obtener_horario():
    guia = conectar_db()
    guia[0].execute("SELECT Hora_Subida FROM shorts ORDER BY Hora_Subida DESC LIMIT 1")
    horario = guia[0].fetchone()
    desconectar_db(guia[1])
    return horario
        
def actualizar_db(tabla, ruta, fecha):
    guia = conectar_db()
    guia[0].execute(f"UPDATE {tabla} SET Estado = 1, Fecha_uso = ? WHERE Ruta = ?", (fecha, ruta,))
    guia[1].commit()
    desconectar_db(guia[1])

def reciclar_archivos(tipo):
    guia = conectar_db()
    guia[0].execute(f"UPDATE {tipo} SET Estado = 0")
    guia[1].commit()
    desconectar_db(guia[1])

def reciclar_memes(categoria):
    guia = conectar_db()
    guia[0].execute("UPDATE Memes SET Estado = 0 WHERE Categoria = ?", (categoria,))
    guia[1].commit()
    desconectar_db(guia[1])

def verificar_nombre(nombre_meme):
    guia = conectar_db()
    guia[0].execute("SELECT 1 FROM Memes WHERE Nombre = ?", (nombre_meme,))
    existe = guia[0].fetchall()
    desconectar_db(guia[1])

    if existe:
        return False
    return True

def verificar_phash(hash_meme):
    guia = conectar_db()
    guia[0].execute("SELECT 1 FROM Memes WHERE Phash = ?", (hash_meme,))
    existe = guia[0].fetchall()
    desconectar_db(guia[1])

    if existe:
        return False
    return True

def registrar(categoria, nombre_meme, hash_meme, Ruta, tiempo):
    guia = conectar_db()
    guia[0].execute("INSERT INTO Memes (Categoria, Nombre, Phash, Ruta, Fecha) VALUES (?, ?, ?, ?, ?)", (categoria, nombre_meme, hash_meme, Ruta, tiempo))
    guia[1].commit()
    desconectar_db(guia[1])