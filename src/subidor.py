from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path
import os
import json
import random
from datetime import datetime

fecha_hoy = datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def autenticacion():
    token = os.path.exists("token.json")
    if token:
        credenciales = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credenciales.json", SCOPES)
        credenciales = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credenciales.to_json())
    return credenciales

def subir_short(ruta_short, categoria):

    credenciales = autenticacion()
    youtube = build("youtube", "v3", credentials=credenciales)

    ruta_json = Path(__file__).parent.parent / "metadata" / f"{categoria}.json"
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    titulo = random.choice(datos["titulos"])
    descripcion = datos["descripcion"][0]
    hashtags = datos["hashtags"][0]

    cuerpo = {
        "snippet": {
            "title": titulo,
            "description": descripcion,
            "tags": hashtags,
            "categoryId": "23",
            "defaultLanguage":"es-419",
            "defaultAudioLanguage": "es-419"
        },
        "status": {
            "privacyStatus": "private"
        },
        "recordingDetails": {
            "localDescription": "Argentina",
            "recordingDate": fecha_hoy
        }
    }

    short = MediaFileUpload(str(ruta_short), mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=cuerpo,
        media_body=short,
    )
    
    id_del_short = None
    try:
        response = request.execute()
        id_del_short = response["id"]
        print("Carga Exitosa")
    except Exception as error:
        print(f"Error técnico detallado de Google: {error}")

    
    return id_del_short