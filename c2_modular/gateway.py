import os
import sys
import json
import subprocess
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from CORE_SHARED.service_discovery import resolve, CircuitBreaker

app = FastAPI(title="C2 Modular - API Gateway", version="3.0")

_NODE_WHITELIST = {}
_SETUP_TOKENS = {}
_FORENSICS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "forensics")
os.makedirs(_FORENSICS_DIR, exist_ok=True)

def _firewall_block(ip):
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], capture_output=True, timeout=5)
    except Exception:
        pass

# ─── Ruta de estado ──────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "module": "c2_modular", "uptime": int(time.time() - _start)}

_start = time.time()

# ─── Mesh Handshake / Heartbeat ──────────────────────────────────────
@app.post("/mesh/handshake")
async def mesh_handshake(request: Request):
    data = await request.json()
    node_ip = request.client.host
    fp = data.get("payload", {}).get("fingerprint", "")
    with threading.Lock():
        for nid, info in list(_NODE_WHITELIST.items()):
            if info.get("fingerprint") == fp:
                return {"ok": True, "node_id": nid, "role": info.get("role", "unknown")}
    _firewall_block(node_ip)
    return {"ok": False, "error": "fingerprint_not_whitelisted"}

@app.post("/mesh/heartbeat")
async def mesh_heartbeat(request: Request):
    data = await request.json()
    node_ip = request.client.host
    with threading.Lock():
        for nid, info in list(_NODE_WHITELIST.items()):
            if info.get("ip") == node_ip:
                info["last_heartbeat"] = time.time()
                return {"ok": True, "node_id": nid}
    _firewall_block(node_ip)
    return {"ok": False, "error": "ip_not_whitelisted"}

@app.get("/mesh/nodes")
async def mesh_nodes():
    with threading.Lock():
        return {"nodos": list(_NODE_WHITELIST.values())}

# ─── Forensic endpoints ──────────────────────────────────────────────
@app.post("/forensic/report")
async def forensic_report(request: Request):
    data = await request.json()
    fname = f"forensic_{int(time.time())}.enc"
    with open(os.path.join(_FORENSICS_DIR, fname), "w") as f:
        f.write(data.get("forensic", ""))
    return {"ok": True, "stored": fname}

@app.post("/forensic/alert")
async def forensic_alert(request: Request):
    data = await request.json()
    log_path = os.path.join(os.path.dirname(_FORENSICS_DIR), "forensic_alerts.log")
    with open(log_path, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ')} [ALERTA FORENSE - NODO {data.get('device_id','?')} - BLOQUEADO] {data.get('reason','')}\n")
    return {"ok": True}

@app.post("/emergency/isolate")
async def emergency_isolate(request: Request):
    data = await request.json()
    log_path = os.path.join(os.path.dirname(_FORENSICS_DIR), "forensic_alerts.log")
    with open(log_path, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ')} [ALERTA FORENSE - NODO {data.get('device_id','?')} - AISLADO]\n")
    return {"ok": True, "device": data.get("device_id"), "status": "isolated"}
