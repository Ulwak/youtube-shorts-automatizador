import os
import requests
import unicodedata
import time
import re
from dotenv import load_dotenv

load_dotenv()
gemini_clave = os.getenv("GEMINI")

def crear_y_realizar_peticion(extension, bytes_base64, categorias):
    categorias_cadena = ", ".join(n for n in categorias)
    if extension != "jpeg":
        extension = extension[-3:]
    url_gemini = (f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={gemini_clave}")
    cabecera = {
        "Content-Type" : "application/json"
    }
    #El prompt ubicado en "systemInstruction": "parts": "text" fue creado utilizando inteligencia artificial para hacer que la IA de
    #gemma unicamente devuelva una palabra y utilizarla para categorizar
    cuerpo = {
        "systemInstruction": {
            "parts": [
                {
                        "text": (
                            f"Sos un categorizador profesional de memes. Tu unica tarea es responder con una sola palabra de esta lista: {categorias_cadena}. Si la imagen contiene contenido sexual o insinuante, esta en ingles responde 'descartado'. Si la imagen no pertenece a ninguna categoria de la lista responde 'varios' No agregues puntos, saludos, ni explicaciones bajo ninguna circunstancia."
                    )
                }
            ]
        },
        "contents" : [
            {
                "parts" : [
                    {
                        "text" : f"Analiza esta imagen. Sos un categorizador profesional de memes. Tu unica tarea es responder con una sola palabra de esta lista: {categorias_cadena}. Si la imagen esta en ingles o contiene contenido sexual responde 'descartado'. Si la imagen no pertenece a ninguna categoria de la lista responde 'varios'. No agregues puntos, saludos, ni explicaciones bajo ninguna circunstancia."
                    },
                    {
                        "inlineData" : {
                            "mimeType" : f"image/{extension}" ,
                            "data" : f"{bytes_base64}"
                        }
                    }
                ]
            }
        ],
    }
    respuesta = requests.post(url_gemini, headers=cabecera, json=cuerpo, timeout=15)
    return respuesta

def obtener_a_que_pertenece(extension, bytes_base64, categorias):
    
    while True:
        try:
            respuesta = crear_y_realizar_peticion(extension, bytes_base64, categorias)
        except:
            respuesta = None
        if respuesta is None:
            print(f"Reintentando petición de red")
            time.sleep(5)
            continue
        if respuesta.status_code != 200:
            print(f"Fallo al realizar la peticion a Gemini {respuesta.status_code}")
            print(f"Respuesta del servidor: {respuesta.text}")
            if respuesta.status_code == 429:
                obtener_tiempo_espera = re.search(r"retry in (\d+\.\d+)s", respuesta.text)
                if obtener_tiempo_espera:
                    tiempo_espera = float(obtener_tiempo_espera.group(1)) + 1.0
                    print(f"Esperando {tiempo_espera} para reintentar y no saturar la API")
                    time.sleep(tiempo_espera)
                    continue
                else:
                    print(f"No se pudo obtener el tiempo de espera especificado por google. Se esperara 20 segundos por defecto para reintentar.")
                    time.sleep(20)
                    continue
            else:
                print("Error de conexion")
                return "descartado"
        else:
            gemini_respuesta = respuesta.json()
            categoria = gemini_respuesta["candidates"][0]["content"]["parts"][0]["text"]
            categoria = categoria.strip()
            categoria = categoria.lower()
            categoria = unicodedata.normalize("NFC", categoria)
            print(f"La IA respondio: {categoria}")
            for carpeta in categorias:
                carpeta_usuario = unicodedata.normalize("NFC", carpeta.strip().lower())
                if categoria == carpeta_usuario:
                    return carpeta
            print(categoria)
            return "descartado"

def llamada_api(extension, bytes_base64, categorias):
    categoria = obtener_a_que_pertenece(extension, bytes_base64, categorias)
    return categoria