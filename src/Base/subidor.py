from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import timedelta
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

def calcular_proximo_horario(obtener_horario):
    horarios = [datetime.strptime(x, "%H:%M").time() for x in ["5:45", "11:45", "17:45", "23:45"]]
    zona_horaria = ZoneInfo("America/Buenos_Aires")
    ultimo_horario = obtener_horario()

    if ultimo_horario is None:
        horario_actual = datetime.now().time()
        dia_actual = datetime.now().date()
        for horario in horarios:
            if horario > horario_actual:
                fecha_y_hora_subida = (datetime.combine(dia_actual, horario, tzinfo=zona_horaria)).isoformat()
                return fecha_y_hora_subida
        dia_siguiente = dia_actual + timedelta(days=1)
        fecha_y_hora_subida = (datetime.combine(dia_siguiente, horarios[0], tzinfo=zona_horaria)).isoformat()
        return fecha_y_hora_subida
    else:
        ultimo_horario = datetime.fromisoformat(ultimo_horario[0]).replace(tzinfo=None)
        dia_ultimo_horario = ultimo_horario.date()
        hora_ultimo_horario = ultimo_horario.time()
        posicion_actual = horarios.index(hora_ultimo_horario)
        posicion_siguiente = (posicion_actual + 1) % 4
        if posicion_siguiente < posicion_actual:
            dia_siguiente = dia_ultimo_horario + timedelta(days=1)
            fecha_y_hora_subida = (datetime.combine(dia_siguiente, horarios[posicion_siguiente], tzinfo=zona_horaria)).isoformat()
            return fecha_y_hora_subida
        else:
            fecha_y_hora_subida = (datetime.combine(dia_ultimo_horario, horarios[posicion_siguiente], tzinfo=zona_horaria)).isoformat()
            return fecha_y_hora_subida

def subir_short(ruta_short, categoria, registrar_shorts, obtener_horario):
    fecha_y_hora_subida = calcular_proximo_horario(obtener_horario)
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
                "privacyStatus": "private",
                "publishAt": fecha_y_hora_subida
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
        registrar_shorts(id_del_short, titulo, fecha_y_hora_subida, fecha_hoy, categoria)
        print("Carga Exitosa")
        return id_del_short
    
    except Exception as error:
        print(f"Error técnico detallado de Google: {error}")
        return None