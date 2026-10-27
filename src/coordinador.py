import sys
import subprocess
from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path

ruta_armador = Path(__file__).parent / "backend" / "armador.py"

server = Flask(__name__)
CORS(server)

@server.route("/ensamblar-short", methods=["POST"])
def llamar_armador():
    respuesta_json = request.get_json()
    datos = []
    for valor in respuesta_json.values():
        datos.append((str(valor)))
    inputs = "\n".join(datos) + "\n"
    short = subprocess.run(
        [sys.executable, str(ruta_armador)],
        input = inputs,
        capture_output = True,
        text = True
        )
    id_del_short = short.stdout.strip().splitlines()
    if id_del_short:
        return jsonify({"respuesta": f"youtube.com/shorts/{id_del_short[-2]}"})
    else:
        return jsonify({"respuesta": "Fallo la subida del short"})

@server.route("/test", methods=["GET"])
def texto():
    return jsonify({"respuesta": f"{5 * 3}"})

if __name__ == '__main__':
    server.run(debug=False, use_reloader=False,  port=8080)