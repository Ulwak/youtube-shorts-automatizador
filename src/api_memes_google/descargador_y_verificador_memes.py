from pathlib import Path
from PIL import Image
from api_memes_google.verificadores_creador_sql import verificar_nombre, verificar_phash, registrar
from api_memes_google.verificador_categoria_google import llamada_api
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
import time
import threading
import base64
import random
import time
import datetime
import requests
import io
import imagehash
import logging

log_descarga_memes = logging.getLogger("descarga_memes")
log_gemini = logging.getLogger("gemini")
log_baseDatos = logging.getLogger("database")
log_ejecucion = logging.getLogger("ejecucion")
log_red = logging.getLogger("red")
lock_datos = threading.Lock()
nombres_en_proceso = set()
phash_en_proceso = set()
tabla_llamadas_api = deque()
lock_rate_api = threading.Lock()

def obtener_urls(shorts_a_crear):
    lista_url = []
    lista_subreddits = ["MemesEnEspanol", "yo_elvr", "MemesESP", "MAAU", "futbol", "BuenosMemesEsp", "MomazosEnEspanol" ]
    sub_reddit = random.choice(lista_subreddits)
    cantidad_memes = shorts_a_crear * 2
    print(f"Sub-reddit elegido: {sub_reddit}")
    if cantidad_memes < 50:
        respuesta = requests.get(f"https://meme-api.com/gimme/{sub_reddit}/{cantidad_memes}", timeout=15)
    else:
        respuesta = requests.get(f"https://meme-api.com/gimme/{sub_reddit}/50", timeout=15)
    try:
        respuesta.raise_for_status()
    except Exception as error_red:
        log_red.info(f"Error de red en la peticion: {error_red}")
        raise
    diccionario = respuesta.json()
    memes = diccionario["memes"]
    for meme in memes:
        url = meme["url"]
        lista_url.append(url)
    return lista_url, sub_reddit

def calculador_Phash(url):
    respuesta = requests.get(url, timeout=15)
    try:
        respuesta.raise_for_status()
    except Exception as error_red:
        log_red.exception(f"Ocurrio un error de red en la peticion: {error_red}")
        raise
    tipo_imagen = respuesta.headers.get("Content-Type", "")
    if not tipo_imagen.startswith("image/"):
        raise ValueError(f"Formato de imagen incorrecto: {tipo_imagen}")
    imagen = io.BytesIO(respuesta.content)
    imagen.seek(0)
    meme = Image.open(imagen)
    try:
        meme.verify()
    except Exception as error_imagen:
        log_descarga_memes.exception(f"Imagen corrupta: {error_imagen}")
        raise
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

def obtener_memes_ya_almacenados():
    ruta_carpetas_memes = Path(__file__).parent.parent.parent / "memes" / "disponibles"
    categorias = [n for n in ruta_carpetas_memes.iterdir() if n.is_dir()]
    stock_memes = {}
    for n in categorias:
        cantidad = len([f for f in (ruta_carpetas_memes / n.name).iterdir() if f.is_file() and not f.name.startswith('.')])
        stock_memes[n.name] = cantidad
    return stock_memes

def filtrado_url_y_cantidad_de_url(lista_url):
    lista_url_limpia = []
    cantidad_url_sin_filtrar = len(lista_url)
    for meme in lista_url:
        if meme[-4:] in [".png", "jpeg", ".jpg"]:
            lista_url_limpia.append(meme)
    cantidad_url_filtrada = len(lista_url_limpia)
    return cantidad_url_sin_filtrar, cantidad_url_filtrada, lista_url_limpia

def registrador_memes(categoria, nombre_meme, imagen, phash, stock_memes, lock):
    try:
        fecha = datetime.date.today()
        fecha = fecha.isoformat()
        with lock:
            guardar_imagen(categoria, nombre_meme, imagen)
            stock_memes[categoria] = stock_memes[categoria] + 1
            registrar(categoria, nombre_meme, phash, fecha)
        log_baseDatos.info(f"Meme {nombre_meme} registrado en la base de datos")
        print("Meme guardado con exito")
        print(f"Categoria del meme: {categoria}")
    except Exception as error_bd:
        print("Error al guardar el meme")
        log_baseDatos.exception(f"Ocurrio un error al guardar en la base de datos: {error_bd}")

def limpieza_llamadas_api(tiempo_ahora):
    while len(tabla_llamadas_api) > 0:
        ultimo_elemento = tabla_llamadas_api[0]
        if (tiempo_ahora - ultimo_elemento) > 60:
            tabla_llamadas_api.popleft()
        else:
            return ultimo_elemento
    
        
def esperar_a_gemini():
    llamada_api_disponible = True
    while llamada_api_disponible:
        tiempo_ahora = time.time()
        with lock_rate_api:
                ultimo_elemento = limpieza_llamadas_api(tiempo_ahora)
                if len(tabla_llamadas_api) >= 15:
                    tiempo_espera = 60 - (tiempo_ahora - ultimo_elemento)
                if len(tabla_llamadas_api) < 15:
                    tabla_llamadas_api.append(tiempo_ahora)
                    llamada_api_disponible = False
                    return
        time.sleep(tiempo_espera)
        log_gemini.info(f"Esperando {tiempo_espera} para evitar saturar la api de Gemini")




def validar_memes(url, subreddit, stock_memes, lock, nombres_en_proceso, phash_en_proceso, lock_rate_api):
    nombre_meme = obtener_nombre_meme(url)
    log_descarga_memes.info(f"[{subreddit}] Procesando meme: {nombre_meme}")
    meme_no_valido = (False, None, None, None, None)
    with lock:
        if nombre_meme in nombres_en_proceso:
            return meme_no_valido
        existe = verificar_nombre(nombre_meme)
        nombres_en_proceso.add(nombre_meme)
    if existe:
        try:
            phash, bytes_base64, imagen = calculador_Phash(url)
            log_descarga_memes.info(f"Calculado el Phash del meme {nombre_meme}")
        except Exception as error_phash:
            print(f"Omitiendo archivo {nombre_meme} por corrupcion o formato invalido")
            log_descarga_memes.exception(f"Ocurrio el siguiente error con el meme {nombre_meme}: {error_phash}")
            return meme_no_valido
        with lock:
            if phash in phash_en_proceso:
                return meme_no_valido
            existe = verificar_phash(phash)
            phash_en_proceso.add(phash)
        if existe:
            extension = url[-4:]
            with lock:
                categorias = list(stock_memes.keys())
            log_descarga_memes.info(f"Listadas las categorias a las que puede corresponder la imagen: {categorias}")
            esperar_a_gemini()
            categoria = llamada_api(extension, bytes_base64, categorias)
            log_descarga_memes.info(f"Realizada la llamada a Gemini para clasificar el meme {nombre_meme}")
            if categoria != "descartado":
                    meme_valido = True
                    log_gemini.info(f"Meme {nombre_meme} clasificado como {categoria} por Gemini")
            else:
                print("Descartado")
                log_descarga_memes.info(f"Meme {nombre_meme} descartado")
                log_gemini.info(f"Meme {nombre_meme} descartado")
                meme_valido = False
        else:
            print(f"El Phash del meme {nombre_meme} ya existe en la base de datos")
            log_descarga_memes.info(f"{nombre_meme} ya existe en la base de datos (Razon: Phash)")
            return meme_no_valido
    else:
        print(f"{nombre_meme} ya existe en la base de datos")
        log_descarga_memes.info(f"{nombre_meme} ya existe en la base de datos (Razon: Nombre)")
        return meme_no_valido
    if meme_valido:
        return meme_valido, categoria, nombre_meme, imagen, phash
    return meme_no_valido
      



def descargador_verificador(shorts_a_crear):
    stock_memes = obtener_memes_ya_almacenados()
    objetivo = shorts_a_crear * 2
    log_ejecucion.info(f"Cantidad de memes requeridos definida ({objetivo})")
    while any(n < objetivo for n in stock_memes.values()):
        lista_url, subreddit = obtener_urls(shorts_a_crear)
        cantidad_url_sin_filtrar, cantidad_url_limpia, lista_url_limpia = filtrado_url_y_cantidad_de_url(lista_url)
        log_ejecucion.info(f"Obtenidas las {cantidad_url_sin_filtrar} URLs de los memes")
        log_ejecucion.info(f"Filtradas las URLs que contenian formatos de imagenes no compatibles. URLs validas: {cantidad_url_limpia}")
        with ThreadPoolExecutor(max_workers=8) as trabajador:
            tareas = [trabajador.submit(validar_memes, i, subreddit, stock_memes, lock_datos, nombres_en_proceso, phash_en_proceso, lock_rate_api) for i in lista_url_limpia]
            for tarea in as_completed(tareas):
                meme_valido, categoria, nombre_meme, imagen, phash = tarea.result()
                if meme_valido:
                    registrador_memes(categoria, nombre_meme, imagen, phash, stock_memes, lock_datos)