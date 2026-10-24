import logging

registro_logs = {
    "youtube": "youtube.log",
    "red": "red.log",
    "shorts": "shorts.log",
    "database": "database.log",
    "inputs_usuario": "inputs_usuario.log",
    "descarga_memes": "descarga_memes.log",
    "api_gemini": "gemini.log",
    "ejecucion": "ejecucion.log",
    "selector": "selector.log",
    "ensamblador": "ensamblador.log",
    "duracion": "duracion.log"
}

def crear_logs(ruta_raiz):
    ruta_logs = ruta_raiz / "logs"
    ruta_logs.mkdir(parents=True, exist_ok=True)
    logs = {}
    for nombre, archivo in registro_logs.items():
        #crea el log
        log = logging.getLogger(nombre)
        #define el nivel del log
        log.setLevel(logging.INFO)
        #comprueba si ya hay handlers del log para evitar duplicado
        if not log.hasHandlers():
        
            escritor = logging.FileHandler(
                ruta_logs / archivo,
                encoding="utf-8"
            )

            formato = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            escritor.setFormatter(formato)
            log.addHandler(escritor)
        
        logs[nombre] = log
    return logs
        