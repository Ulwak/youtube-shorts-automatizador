from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from verificadores_creadores_sql import verificar_nombre, verificar_phash, registrar
import requests
import json
import io
import imagehash

respuesta = requests.get("https://meme-api.com/gimme/MemesEnEspanol/50")
diccionario = respuesta.json()

def obtener_urls(diccionario):
    lista_url = []
    cantidad_memes = diccionario["memes"]
    for meme in cantidad_memes:
        url = meme["url"]
        lista_url.append(url)
    return lista_url

def calculador_Phash(url):
    imagen = requests.get(url).content
    imagen = io.BytesIO(imagen)
    imagen.seek(0)
    meme = Image.open(imagen)
    phash = str(imagehash.phash(meme))
    return phash

def descargador_verificador():
    lista_url = obtener_urls()
    for meme in lista_url:
        existe = verificar_nombre(meme)
        if existe:
            phash = calculador_Phash(meme)
            existe = verificar_phash(phash)
            if existe:
                registrar(meme, phash)
            