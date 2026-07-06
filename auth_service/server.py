import os, sys, json, time, uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth_service.database import init, register, login, approve, reject, pending, store_token, verify_token

app = FastAPI(title="Auth Service", version="2.0")
C2 = os.getenv("C2_ENDPOINT", "http://c2_gateway:9090")

class RegPayload(BaseModel): email: str; username: str; password: str
class LoginPayload(BaseModel): email: str; password: str
class IdPayload(BaseModel): user_id: int; admin_id: str = "admin"
class TokenPayload(BaseModel): token: str

def _alert_c2(uid, email, username):
    try:
        import urllib.request
        d = json.dumps({"reason": "new_preregister", "device_id": "auth", "type": "registration_pending", "timestamp": time.time(), "metadata": {"user_id": uid, "email": email, "username": username}}).encode()
        r = urllib.request.Request(f"{C2}/forensic/alert", data=d, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(r, timeout=5)
    except: pass

@app.on_event("startup")
def startup(): init(); print("[AUTH] Base de datos inicializada")

@app.post("/auth/register")
async def do_register(p: RegPayload):
    r = register(p.email, p.username, p.password)
    if not r.get("ok"): raise HTTPException(409, r.get("error", "registration_failed"))
    _alert_c2(r["user_id"], p.email, p.username)
    return {"status": "pending", "user_id": r["user_id"], "message": "Registro pendiente de aprobacion"}

@app.post("/auth/login")
async def do_login(p: LoginPayload):
    u = login(p.email, p.password)
    if not u: raise HTTPException(401, "Credenciales invalidas")
    if u["estado"] != "Activo": raise HTTPException(403, f"Cuenta {u['estado']}")
    t = uuid.uuid4().hex
    store_token(u["id"], t)
    return {"status": "ok", "user_id": u["id"], "rol": u["rol"], "username": u["username"], "token": t}

@app.post("/auth/approve")
async def do_approve(p: IdPayload):
    if not approve(p.user_id, p.admin_id): raise HTTPException(404, "No encontrado o ya aprobado")
    return {"status": "ok", "message": "Usuario aprobado"}

@app.post("/auth/reject")
async def do_reject(p: IdPayload):
    if not reject(p.user_id): raise HTTPException(404, "No encontrado")
    return {"status": "ok", "message": "Usuario rechazado"}

@app.get("/auth/pending")
async def list_pending():
    return {"pendientes": pending()}

@app.post("/auth/verify")
async def verify(p: TokenPayload):
    uid = verify_token(p.token)
    return {"ok": uid is not None, "user_id": uid}

@app.get("/auth/health")
async def health():
    return {"status": "ok", "service": "auth_service"}
