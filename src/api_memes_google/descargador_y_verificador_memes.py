from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from api_memes_google.verificadores_creador_sql import verificar_nombre, verificar_phash, registrar
from api_memes_google.verificador_categoria_google import llamada_api
import base64
import time
import datetime
import requests
import io
import imagehash

def obtener_urls(shorts_a_crear):
    lista_url = []
    cantidad_memes = shorts_a_crear * 2
    if cantidad_memes < 50:
        respuesta = requests.get(f"https://meme-api.com/gimme/MemesEnEspanol/{cantidad_memes}")
    else:
        respuesta = requests.get("https://meme-api.com/gimme/MemesEnEspanol/50")
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
    
        memes_enviados_api = 0

        for meme in lista_url_limpia:
            nombre_meme = obtener_nombre_meme(meme)
            existe = verificar_nombre(nombre_meme)
            if existe:
                phash_bytes64 = calculador_Phash(meme)
                existe = verificar_phash(phash_bytes64[0])
                if existe:
                    extension = meme[-4:]
                    categoria = llamada_api(extension, phash_bytes64[1]) 
                    if categoria != "descartado":
                        try:
                            fecha = datetime.date.today()
                            fecha = fecha.isoformat()
                            guardar_imagen(categoria, nombre_meme, phash_bytes64[2])
                            stock_memes[categoria] = stock_memes[categoria] + 1
                            registrar(categoria, nombre_meme, phash_bytes64[0], fecha)
                            memes_enviados_api = memes_enviados_api + 1
                            print("Meme guardado con exito")
                        except:
                            print("Error al guardar")
                    memes_enviados_api = memes_enviados_api + 1
                    if memes_enviados_api == 15:
                            print("Esperando 15 segundos para no saturar a la API de google")
                            time.sleep(15)
                            print("Espera terminada, reanudando")
                            memes_enviados_api = 0
            