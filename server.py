from flask import Flask, jsonify, request, abort
import json
import os
import datetime
import hmac
import hashlib
import base64
import sqlite3

app = Flask(__name__)
DB_PATH = "kexpler_cloud.db"

# --- INICIO KERNEL JOSAMICK (Supervisor) ---

class JosamickKernel:

    def __init__(self):
        self.bitacora = []
        self.modulos = {
            "kernel": "activo",
            "oceanic": "standby",
            "wallet": "standby",
            "scout": "standby"
        }
        self._log_dir = "kernel_logs"
        os.makedirs(self._log_dir, exist_ok=True)
        self.oceanic = None
        self.verificar_integridad()

    def registrar_evento(self, evento, origen="kernel"):
        ts = datetime.datetime.now().isoformat()
        entrada = {"timestamp": ts, "evento": evento, "origen": origen}
        self.bitacora.append(entrada)
        log_path = os.path.join(self._log_dir, f"eventos_{datetime.date.today().isoformat()}.log")
        with open(log_path, "a") as f:
            f.write(json.dumps(entrada) + "\n")

    def verificar_integridad(self):
        try:
            assert os.path.isdir(self._log_dir), "log_dir no accesible"
            self.registrar_evento("integridad_ok", "kernel")
            self._integridad = "ok"
        except Exception as e:
            self._integridad = f"fallo: {e}"

    def interceptar_llamada(self, mod_origen, accion):
        self.registrar_evento(f"interceptada:{accion}", mod_origen)
        return {"autorizado": True, "modulo": mod_origen, "accion": accion}

    def obtener_estado(self):
        return {
            "modulos": self.modulos,
            "integridad": getattr(self, "_integridad", "no_verificada"),
            "eventos_registrados": len(self.bitacora)
        }

    def salida_cifrada(self, datos):
        if self.oceanic:
            return self.oceanic.encriptar(json.dumps(datos))
        return datos


kernel = JosamickKernel()

# --- INICIO SEGURIDAD OCEANIC (Cifrado) ---

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes

class OceanicShield:

    def __init__(self, clave_maestra=None):
        if clave_maestra is None:
            clave_maestra = os.urandom(32)
        elif isinstance(clave_maestra, str):
            clave_maestra = clave_maestra.encode()[:32].ljust(32, b'\0')
        self._clave = clave_maestra[:32] if len(clave_maestra) >= 32 else clave_maestra.ljust(32, b'\0')
        self._clave_firma = hashlib.sha256(self._clave).digest()
        self.aes = AESGCM(self._clave)

    def encriptar(self, datos):
        if isinstance(datos, str):
            datos = datos.encode("utf-8")
        nonce = os.urandom(12)
        cifrado = self.aes.encrypt(nonce, datos, None)
        return base64.b64encode(nonce + cifrado).decode("utf-8")

    def desencriptar(self, datos_cifrados):
        try:
            raw = base64.b64decode(datos_cifrados.encode("utf-8"))
            nonce, cifrado = raw[:12], raw[12:]
            return self.aes.decrypt(nonce, cifrado, None).decode("utf-8")
        except Exception:
            return None

    def firmar_paquete(self, datos):
        if isinstance(datos, str):
            datos = datos.encode("utf-8")
        return hmac.new(self._clave_firma, datos, hashlib.sha256).hexdigest()

    def verificar_firma(self, datos, firma):
        if isinstance(datos, str):
            datos = datos.encode("utf-8")
        return hmac.compare_digest(self.firmar_paquete(datos), firma)


CLAVE_MAESTRA = os.environ.get("JOSAMICK_MASTER_KEY", "clave_maestra_predeterminada")
oceanic = OceanicShield(CLAVE_MAESTRA)
kernel.oceanic = oceanic
kernel.modulos["oceanic"] = "activo"
kernel.registrar_evento("oceanic_shield_activado", "oceanic")


@app.before_request
def middleware_oceanic():
    if request.path.startswith("/api/") and request.method in ("POST", "PUT"):
        firma = request.headers.get("X-Oceanic-Firma")
        if not firma:
            abort(401, {"error": "Firma Oceanic requerida"})
        body = request.get_data(as_text=True)
        if not oceanic.verificar_firma(body, firma):
            abort(403, {"error": "Firma Oceanic invalida"})
        kernel.interceptar_llamada("oceanic", f"request:{request.path}")

# --- INICIO MOTOR FINANCIERO (Wallet/Ledger) ---

def init_wallet_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0.0,
            external_address TEXT DEFAULT ''
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ledger_transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emisor_id INTEGER NOT NULL,
            receptor_id INTEGER NOT NULL,
            monto REAL NOT NULL,
            monto_receptor REAL NOT NULL,
            monto_plataforma REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            hash_oceanic TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def obtener_saldo(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT balance FROM wallet WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0.0

def actualizar_saldo(user_id, delta):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO wallet (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?", (user_id, delta, delta))
    conn.commit()
    conn.close()

def procesar_transferencia(emisor, receptor, monto):
    if monto <= 0:
        return {"status": "error", "msg": "Monto invalido"}
    monto_receptor = round(monto * 0.95, 2)
    monto_plataforma = round(monto - monto_receptor, 2)
    payload = json.dumps({"emisor": emisor, "receptor": receptor, "monto": monto, "ts": str(datetime.datetime.now())}, sort_keys=True)
    hash_oceanic = oceanic.firmar_paquete(payload)
    actualizar_saldo(emisor, -monto)
    actualizar_saldo(receptor, monto_receptor)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ledger_transacciones (emisor_id, receptor_id, monto, monto_receptor, monto_plataforma, hash_oceanic)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (emisor, receptor, monto, monto_receptor, monto_plataforma, hash_oceanic))
    conn.commit()
    conn.close()
    kernel.registrar_evento(f"transferencia:{hash_oceanic[:12]}", "wallet")
    return {"status": "exito", "hash_oceanic": hash_oceanic, "monto_receptor": monto_receptor, "monto_plataforma": monto_plataforma}

init_wallet_db()
kernel.modulos["wallet"] = "activo"
kernel.registrar_evento("wallet_engine_activado", "wallet")

@app.route('/api/wallet/balance', methods=['GET'])
def get_balance():
    user_id = request.args.get('user_id', 1, type=int)
    balance = obtener_saldo(user_id)
    payload = json.dumps({"user_id": user_id, "balance": balance})
    cifrado = oceanic.encriptar(payload)
    firma = oceanic.firmar_paquete(cifrado)
    return jsonify({"data_cifrada": cifrado, "firma": firma})

@app.route('/api/wallet/donar', methods=['POST'])
def donar():
    data = request.json
    emisor = data.get('emisor_id')
    receptor = data.get('receptor_id')
    monto = data.get('monto')
    resultado = procesar_transferencia(emisor, receptor, monto)
    if resultado["status"] == "error":
        return jsonify(resultado), 400
    return jsonify(resultado)

# --- INICIO SISTEMA SCOUT/REFERRAL ---

import secrets

def init_scout_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS referidos (
            user_id INTEGER PRIMARY KEY,
            codigo_referido TEXT UNIQUE,
            referido_por_id INTEGER,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tareas_scout (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            recompensa REAL,
            completada INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def generar_codigo():
    return "JSM" + secrets.token_hex(4).upper()

def aplicar_codigo_referido(usuario, codigo):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM referidos WHERE codigo_referido = ?", (codigo,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return {"status": "error", "msg": "Codigo invalido"}
    referido_por = row[0]
    cur.execute("INSERT OR IGNORE INTO referidos (user_id, codigo_referido, referido_por_id) VALUES (?, ?, ?)",
                (usuario, generar_codigo(), referido_por))
    conn.commit()
    conn.close()
    kernel.registrar_evento(f"referido:{usuario}<-{referido_por}", "scout")
    procesar_transferencia(referido_por, usuario, 10)
    return {"status": "exito", "bonus": 10, "msg": "Usuario vinculado. Bono de 10 aplicado."}

init_scout_db()
kernel.modulos["scout"] = "activo"
kernel.registrar_evento("scout_engine_activado", "scout")

@app.route('/api/scout/buscar', methods=['GET'])
def scout_buscar():
    intercept = kernel.interceptar_llamada("scout", "buscar_tareas")
    if not intercept.get("autorizado"):
        return jsonify({"status": "bloqueado", "msg": "Kernel denego la operacion"}), 403
    tareas = [
        {"id": 1, "descripcion": "Reportar vulnerabilidad en red local", "recompensa": 50},
        {"id": 2, "descripcion": "Completar perfil de nodo", "recompensa": 15},
        {"id": 3, "descripcion": "Invitacion valida de nuevo usuario", "recompensa": 25},
    ]
    payload = json.dumps({"tareas": tareas, "scout": "activo"})
    cifrado = oceanic.encriptar(payload)
    firma = oceanic.firmar_paquete(cifrado)
    return jsonify({"data_cifrada": cifrado, "firma": firma})

@app.route('/api/scout/completar', methods=['POST'])
def scout_completar():
    data = request.json
    tarea_id = data.get("tarea_id")
    user_id = data.get("user_id")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT recompensa FROM tareas_scout WHERE id = ? AND completada = 0", (tarea_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"status": "error", "msg": "Tarea no disponible"}), 400
    recompensa = row[0]
    cur.execute("UPDATE tareas_scout SET completada = 1 WHERE id = ?", (tarea_id,))
    conn.commit()
    conn.close()
    resultado_pago = procesar_transferencia(0, user_id, recompensa)
    return jsonify({"status": "completada", "pago": resultado_pago})

@app.route('/api/referido/codigo', methods=['GET'])
def obtener_codigo():
    user_id = request.args.get('user_id', 1, type=int)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT codigo_referido FROM referidos WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        codigo = row[0]
    else:
        codigo = generar_codigo()
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO referidos (user_id, codigo_referido) VALUES (?, ?)", (user_id, codigo))
        conn.commit()
        conn.close()
    payload = json.dumps({"user_id": user_id, "codigo": codigo, "enlace": f"/registro?ref={codigo}"})
    cifrado = oceanic.encriptar(payload)
    firma = oceanic.firmar_paquete(cifrado)
    return jsonify({"data_cifrada": cifrado, "firma": firma})

@app.route('/api/referido/vincular', methods=['POST'])
def referido_vincular():
    data = request.json
    usuario = data.get("user_id")
    codigo = data.get("codigo")
    return jsonify(aplicar_codigo_referido(usuario, codigo))


@app.route('/')
def home():
    return jsonify({'status': 'Sistema Kexpler en linea', 'kernel': 'Esperando instrucciones'})

@app.route('/api/kernel/status')
def kernel_status():
    estado = kernel.obtener_estado()
    datos_salida = oceanic.encriptar(json.dumps(estado))
    return jsonify({"status_cifrado": datos_salida, "firma": oceanic.firmar_paquete(datos_salida)})

if __name__ == '__main__':
    print("[OK] Kernel Josamick inyectado y operativo.")
    print(f"[KERNEL] Integridad: {kernel._integridad}")
    print(f"[OCEANIC] Shield activo — AES-256-GCM + HMAC-SHA256")
    print(f"[WALLET] Ledger + Split 95/5 operativo")
    print(f"[SCOUT] Motor de crecimiento activo — Referral + Busqueda")
    app.run(host='0.0.0.0', port=5000, debug=True)
