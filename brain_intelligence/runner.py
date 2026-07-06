import os, sys, json, time, threading, urllib.request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
C2 = os.getenv("C2_ENDPOINT", "http://c2_gateway:9090")

def _post(path, data):
    try:
        r = urllib.request.Request(f"{C2}{path}", data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except: return {"ok": False}

def _heartbeat():
    while True:
        _post("/mesh/heartbeat", {"node_id": "brain", "timestamp": time.time(), "uptime": 0, "cpu_load": 0.0})
        time.sleep(30)

if __name__ == "__main__":
    print("[BRAIN] Nucleo de inteligencia iniciado")
    _post("/mesh/handshake", {"payload": {"node_id": "brain", "fingerprint": os.getenv("MESH_FINGERPRINT", "brain_fp")}, "firma": "internal"})
    t = threading.Thread(target=_heartbeat, daemon=True)
    t.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("[BRAIN] Detenido.")
