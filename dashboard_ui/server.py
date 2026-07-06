import os, sys, json, urllib.request

from flask import Flask, render_template, request, jsonify

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
app = Flask(__name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "JOSAMICK", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "JOSAMICK", "static"))

AUTH = os.getenv("AUTH_ENDPOINT", "http://auth:8001")

def _proxy(path, data):
    try:
        r = urllib.request.Request(f"{AUTH}{path}", data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except: return {"status": "error", "detail": "auth_service_unreachable"}

@app.route("/")
def index():
    return render_template("kexpler.html")

@app.route("/registro")
def registro():
    return render_template("register.html")

@app.route("/api/network/register", methods=["POST"])
def api_register():
    d = request.json
    r = _proxy("/auth/register", {"email": d.get("email"), "username": d.get("username"), "password": d.get("password")})
    return jsonify(r), (200 if r.get("status") == "pending" else 409)

@app.route("/api/network/login", methods=["POST"])
def api_login():
    d = request.json
    r = _proxy("/auth/login", {"email": d.get("email", d.get("username")), "password": d.get("password")})
    return jsonify(r), (200 if r.get("status") == "ok" else 401)

if __name__ == "__main__":
    h = os.getenv("KEXPLER_HOST", "0.0.0.0")
    p = int(os.getenv("KEXPLER_PORT", "5002"))
    print(f"[DASHBOARD] Interfaz web en puerto {p}")
    app.run(host=h, port=p, debug=False)
