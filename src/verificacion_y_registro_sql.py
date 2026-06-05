import sqlite3
from pathlib import Path

ruta_db = Path(__file__).parent.parent / "database" / "registro.db"

def conectar_db():
    conectado = sqlite3.connect(ruta_db)
    guia = conectado.cursor()
    return guia, conectado

def desconectar_db(conectado):
    conectado.close()

def iniciar_db():
    ruta_sql = Path(__file__).parent.parent / "database" / "registro.sql"
    
    guia = conectar_db()

    with open(ruta_sql, "r") as sql:
        codigo_sql = sql.read()

    guia[0].executescript(codigo_sql)
    
    guia[1].commit()
    desconectar_db(guia[1])
    
def verificar_nombre(nombre_meme):
    guia = conectar_db()
    guia[0].execute("SELECT 1 FROM Memes WHERE Nombre = ?", (nombre_meme,))
    existe = guia[0].fetchall()
    desconectar_db(guia[1])


    if existe:
        return True  
    return False

def verificar_phash(hash_meme):
    guia = conectar_db()
    guia[0].execute("SELECT 1 FROM Memes WHERE Phash = ?", (hash_meme,))
    existe = guia[0].fetchall()
    desconectar_db(guia[1])

    if existe:
        return True
    return False

def registrar(categoria, nombre_meme, hash_meme):
    guia = conectar_db()
    guia[0].execute("INSERT INTO Memes (Categoria, Nombre, Phash) VALUES (?, ?, ?)", (categoria, nombre_meme, hash_meme,))
    guia[1].commit()
    desconectar_db(guia[1])
    


def main():
    iniciar_db()

if __name__ == "__main__":
    main()