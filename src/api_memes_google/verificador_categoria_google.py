import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
gemini_clave = os.getenv("GEMINI")

def crear_y_realizar_peticion(extension, bytes_base64):
    if extension != "jpeg":
        extension = extension[-3:]
    url_gemini = ("https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + gemini_clave)
    cabecera = {
        "Content-Type" : "application/json"
    }

    cuerpo = {
        "contents" : [
            {
                "parts" : [
                    {   #Este prompt fue creado utilizando inteligencia artificial para hacer que la IA de
                        #gemini unicamente devuelva una palabra y utilizarla para categorizar
                        "text" : "Analiza esta imagen. Responde con una unica palabra de esta lista si el meme pertenece a alguna de estas categorias: 'escuela', 'firulais', 'michis', 'videojuegos'. Si la imagen no es un meme humoristico, esta en ingles, o no encaja perfectamente en ninguna, responde estrictamente: 'descartado'. No agregues puntos, saludos ni explicaciones."
                    },
                    {
                        "inlineData" : {
                            "mimeType" : f"image/{extension}" ,
                            "data" : f"{bytes_base64}"
                        }
                    }
                
                ]
            }
        ]     
    }
    respuesta = requests.post(url_gemini, headers=cabecera, json=cuerpo)
    return respuesta

def obtener_a_que_pertenece(respuesta):
    gemini_respuesta = respuesta.json()
    categoria = gemini_respuesta["candidates"][0]["content"]["parts"][0]["text"]
    categoria = categoria.strip()
    categoria = categoria.lower()
    return categoria

def llamada_api(extension, bytes_base64):
    respuesta = crear_y_realizar_peticion(extension, bytes_base64)
    categoria = obtener_a_que_pertenece(respuesta)
    return categoria


