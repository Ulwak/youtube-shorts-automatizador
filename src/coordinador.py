from flask import Flask, jsonify
from flask_cors import CORS


server = Flask(__name__)
CORS(server)

@server.route("/ensamblar-short", methods=["GET"])
def llamar_armador():
    pass

@server.route("/test", methods=["GET"])
def texto():
    return jsonify({"respuesta": f"{5 * 3}"})

if __name__ == '__main__':
    server.run(debug=True, port=8080)