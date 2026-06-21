from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from api_memes_google.verificadores_creador_sql import verificar_nombre, verificar_phash, registrar
from api_memes_google.verificador_categoria_google import llamada_api
import base64
import random
import time
import datetime
import requests
import io
import imagehash

def obtener_urls(shorts_a_crear):
    lista_url = []
    lista_subreddits = ["MemesEnEspanol", "yo_elvr", "MemesESP", "MAAU", "PerrosArgentinos", "futbol", "BuenosMemesEsp", "MomazosEnEspanol" ]
    sub_reddit = random.choice(lista_subreddits)
    cantidad_memes = shorts_a_crear * 2
    print(f"Sub-reddit elegido: {sub_reddit}")
    if cantidad_memes < 50:
        respuesta = requests.get(f"https://meme-api.com/gimme/{sub_reddit}/{cantidad_memes}")
    else:
        respuesta = requests.get(f"https://meme-api.com/gimme/{sub_reddit}/50")
    diccionario = respuesta.json()
    memes = diccionario["memes"]
    for meme in memes:
        url = meme["url"]
        lista_url.append(url)
    return lista_url

def calculador_Phash(url):
    imagen = requests.get(url).content
    imagen = io.BytesIO(imagen)
    imagen.seek(0)
    meme = Image.open(imagen)
    phash = str(imagehash.phash(meme))
    bytes_base64 = imagen.getvalue()
    bytes_base64 = base64.b64encode(bytes_base64).decode('utf-8')
    return phash, bytes_base64, imagen

def obtener_nombre_meme(url):
    url_fraccionada = url.split("/")
    nombre = url_fraccionada[-1]
    return nombre

def guardar_imagen(categoria, nombre_meme, imagen):
    carpeta_categoria = Path(__file__).parent.parent.parent / "memes" / "disponibles" / categoria
    carpeta_categoria.mkdir(parents=True, exist_ok=True)
    ruta_meme = carpeta_categoria / nombre_meme
    imagen.seek(0)
    with open(ruta_meme, "wb") as meme:
        meme.write(imagen.read())
    return

def obtener_memes_ya_almacenados():
    ruta_carpetas_memes = Path(__file__).parent.parent.parent / "memes" / "disponibles"
    categorias = [n for n in ruta_carpetas_memes.iterdir() if n.is_dir()]
    stock_memes = {}
    for n in categorias:
        cantidad = len([f for f in (ruta_carpetas_memes / n.name).iterdir() if f.is_file() and not f.name.startswith('.')])
        stock_memes[n.name] = cantidad
    return stock_memes

def descargador_verificador(shorts_a_crear):
    stock_memes = obtener_memes_ya_almacenados()
    objetivo = shorts_a_crear * 2
    while any(n < objetivo for n in stock_memes.values()):
        lista_url = obtener_urls(shorts_a_crear)
        lista_url_limpia = []
        for meme in lista_url:
            extension = meme[-4:]
            if extension in[".png", "jpeg", ".jpg"]:
                lista_url_limpia.append(meme)
    
        for meme in lista_url_limpia:
            nombre_meme = obtener_nombre_meme(meme)
            existe = verificar_nombre(nombre_meme)
            if existe:
                try:
                    phash_bytes64 = calculador_Phash(meme)
                except Exception as error:
                    print(f"Omitiendo archivo por corrupcion o formato invalido (Error: {error})")
                    continue
                existe = verificar_phash(phash_bytes64[0])
                if existe:
                    extension = meme[-4:]
                    categorias = list(stock_memes.keys())
                    categoria = llamada_api(extension, phash_bytes64[1], categorias) 
                    if categoria != "descartado":
                        try:
                            fecha = datetime.date.today()
                            fecha = fecha.isoformat()
                            guardar_imagen(categoria, nombre_meme, phash_bytes64[2])
                            stock_memes[categoria] = stock_memes[categoria] + 1
                            registrar(categoria, nombre_meme, phash_bytes64[0], fecha)
                            print("Meme guardado con exito")
                            print(categoria)
                        except Exception as Error:
                            print(f"Error '{Error}' al guardar")
                    else:
                        print("Descartado")
                else:
                    print("El Phash ya existe en la base de datos")
            else:
                print("El nombre del meme ya existe en la base de datos")
            print("Esperando 2 segundos para no saturar a la API")
            time.sleep(2)