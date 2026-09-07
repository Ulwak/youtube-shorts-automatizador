from api_memes_google.verificadores_creador_sql import actualizador_datos_db_primera_vez
from pathlib import Path
#Esta desprolijo porque fue escrito a ultimo momento para solventar el problema de que el programa no leia los archivos de las carpetas del usuario
#para que la DB sepa que tenia.
def main():
    tablas = ["musica", "likes", "fondos", "comentarios"]
    for i in tablas:
        ruta = Path(__file__).parent.parent / i
        archivo_2 = [n for n in ruta.iterdir() if n.is_file() and not n.name.startswith('.')]
        for n in archivo_2:
            actualizador_datos_db_primera_vez(i, n.name, str(n))

if __name__ == "__main__":
    main()