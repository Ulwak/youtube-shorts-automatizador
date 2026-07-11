from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from pathlib import Path
import json
import random
from datetime import datetime, UTC

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def autenticacion():
    token_ruta = Path(__file__).parent / "token.json"
    credenciales_ruta = Path(__file__).parent / "credenciales.json"
    if token_ruta.exists():
        credenciales = Credentials.from_authorized_user_file(str(token_ruta), SCOPES)
        if credenciales.expired:
            if not credenciales.refresh_token:
                token_ruta.unlink()
                return autenticacion() 
            try:
                credenciales.refresh(Request())
            except Exception:
                token_ruta.unlink()
                return autenticacion()
            with open(token_ruta, "w") as token_archivo:
                token_archivo.write(credenciales.to_json())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credenciales_ruta, SCOPES)
        credenciales = flow.run_local_server(port=0)
        with open(token_ruta, "w") as token_archivo:
            token_archivo.write(credenciales.to_json())
    return credenciales

def subir_short(ruta_short, categoria):
    try:
        credenciales = autenticacion()
        youtube = build("youtube", "v3", credentials=credenciales)

        ruta_json = Path(__file__).parent.parent.parent / "metadata" / "metadata.json"
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
        
        datos = contenido[categoria]

        titulo = random.choice(datos["titulos"])
        descripcion = datos["descripcion"][0]
        hashtags = datos["hashtags"][0].split()
        fecha_hoy = datetime.now(UTC).strftime('%Y-%m-%dT00:00:00Z')

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
                "locationDescription": "Argentina",
                "recordingDate": fecha_hoy
            }
        }

        short = MediaFileUpload(str(ruta_short), mimetype="video/mp4", resumable=True)

        request = youtube.videos().insert(
            part="snippet,status,recordingDetails",
            body=cuerpo,
            media_body=short,
        )
    
        response = request.execute()
        id_del_short = response["id"]
        print("Carga Exitosa")
        return id_del_short
    
    except Exception as error:
        print(f"Error técnico detallado de Google: {error}")
        return None