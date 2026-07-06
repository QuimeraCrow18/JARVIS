import os, sys, json, time, hmac, hashlib, uuid, subprocess, urllib.request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="C2 Gateway", version="3.1")
_start = time.time()
AUTH_ENDPOINT = os.getenv("AUTH_ENDPOINT", "http://auth:8001")
ADMIN_KEY = os.getenv("C2_ADMIN_KEY", "JOSAMICK_C2_ADMIN")
C2_TOKEN = ""
_FORENSICS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "forensics")
os.makedirs(_FORENSICS, exist_ok=True)
_NODES = {}

class AuthPayload(BaseModel): key: str
class ForensicPayload(BaseModel): forensic: str
class AlertPayload(BaseModel): reason: str; device_id: str; type: str; timestamp: float
class HandshakePayload(BaseModel): payload: dict; firma: str

def _verify_auth(token):
    try:
        r = urllib.request.Request(f"{AUTH_ENDPOINT}/auth/verify", data=json.dumps({"token": token}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=5) as resp:
            return json.loads(resp.read().decode()).get("ok", False)
    except: return False

def _fw_block(ip):
    try: subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], capture_output=True, timeout=5)
    except: pass

@app.get("/health")
async def health():
    return {"status": "ok", "service": "c2_gateway", "uptime": int(time.time() - _start)}

@app.get("/", include_in_schema=False)
async def root():
    return {"service": "C2 Gateway — Centro de Mando", "status": "online"}

@app.post("/auth/login")
async def login(p: AuthPayload):
    global C2_TOKEN
    if p.key == ADMIN_KEY or hmac.compare_digest(p.key, ADMIN_KEY):
        C2_TOKEN = uuid.uuid4().hex
        return {"ok": True, "token": C2_TOKEN}
    raise HTTPException(403, "Clave maestra invalida")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not _verify_auth(request.headers.get("x-auth-token", "")):
        raise HTTPException(401, "Token invalido")
    html = "<h1>C2 Gateway — Dashboard</h1><p>Autenticado. Panel de control del ecosistema.</p>"
    return html

@app.post("/mesh/handshake")
async def handshake(p: HandshakePayload, req: Request):
    fp = p.payload.get("fingerprint", "")
    for nid, info in _NODES.items():
        if info.get("fingerprint") == fp:
            return {"ok": True, "node_id": nid, "role": info.get("role", "unknown")}
    _fw_block(req.client.host)
    return {"ok": False, "error": "not_whitelisted"}

@app.post("/mesh/heartbeat")
async def heartbeat(req: Request):
    data = await req.json()
    ip = req.client.host
    for nid, info in _NODES.items():
        if info.get("ip") == ip:
            info["last_heartbeat"] = time.time()
            return {"ok": True, "node_id": nid}
    _fw_block(ip)
    return {"ok": False, "error": "unknown_ip"}

@app.get("/mesh/nodes")
async def nodes():
    return {"nodos": list(_NODES.values())}

@app.post("/forensic/report")
async def forensic_report(p: ForensicPayload):
    fname = f"forensic_{int(time.time())}.enc"
    with open(os.path.join(_FORENSICS, fname), "w") as f:
        f.write(p.forensic)
    return {"ok": True, "stored": fname}

@app.post("/forensic/alert")
async def forensic_alert(p: AlertPayload):
    log = os.path.join(os.path.dirname(_FORENSICS), "forensic_alerts.log")
    with open(log, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ')} [ALERTA FORENSE - NODO {p.device_id} - BLOQUEADO] {p.reason}\n")
    return {"ok": True}
