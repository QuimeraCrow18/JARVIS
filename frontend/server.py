import os
import sys
from flask import Flask, render_template

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "JOSAMICK", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "JOSAMICK", "static"))

@app.route("/")
def index():
    return render_template("kexpler.html")

if __name__ == "__main__":
    host = os.getenv("FRONTEND_HOST", "0.0.0.0")
    port = int(os.getenv("FRONTEND_PORT", "5002"))
    print(f"[FRONTEND] Interfaz web en puerto {port}")
    app.run(host=host, port=port, debug=True)
