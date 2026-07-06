import os
import sys
from flask import Flask, render_template, jsonify, request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CORE_SHARED.security.oceanic_shield import OceanicShield

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'JOSAMICK', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'JOSAMICK', 'static'))

@app.route('/')
def kexpler_home():
    return render_template('kexpler.html')

@app.route('/api/network/register', methods=['POST'])
def register_user():
    data = request.json
    return jsonify({"status": "success", "message": "Usuario registrado en la red criptografica"})

@app.route('/api/network/login', methods=['POST'])
def login_user():
    data = request.json
    return jsonify({"status": "success", "message": "Acceso concedido al nodo Kexpler"})

if __name__ == '__main__':
    _host = os.getenv("KEXPLER_HOST", "0.0.0.0")
    _port = int(os.getenv("KEXPLER_PORT", "5002"))
    _debug = os.getenv("KEXPLER_DEBUG", "true").lower() == "true"
    print(f"[KEXPLER] Nodo Red Social activo en puerto {_port}")
    app.run(host=_host, port=_port, debug=_debug)
