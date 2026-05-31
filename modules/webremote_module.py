import os
import json
import threading
import io
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

from core.utils import safe_method


WEB_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ui", "web"
)


class WebRemoteModule:

    def __init__(self, host="0.0.0.0", port=8080):

        self.host = host
        self.port = port
        self._server = None
        self._thread = None
        self._running = False
        self.jarvis_refs = {}

        self._flask_available = False
        self._check_flask()

        print(f"[WEB] Módulo web remote iniciado (puerto {port}).")

    def _check_flask(self):

        try:
            import flask
            self._flask_available = True
            print("[WEB] Flask disponible - Modo API completo.")
        except ImportError:
            self._flask_available = False
            print("[WEB] Flask no disponible - Usando http.server (básico).")

    @safe_method
    def register_jarvis(self, **refs):

        self.jarvis_refs.update(refs)
        print(f"[WEB] Referencias registradas: {list(refs.keys())}")

    @safe_method
    def start(self):

        if self._running:
            print("[WEB] Servidor ya está corriendo.")
            return

        if self._flask_available:
            self._start_flask()
        else:
            self._start_stdlib()

        self._running = True
        print(f"[WEB] Servidor en http://{self.host}:{self.port}")
        print(f"[WEB] Accede desde cualquier dispositivo en la red.")

    def _start_flask(self):

        from flask import Flask, jsonify, request, send_from_directory

        app = Flask(__name__, static_folder=None)

        refs = self.jarvis_refs

        @app.route("/")
        def index():
            return send_from_directory(WEB_DIR, "index.html")

        @app.route("/static/<path:filename>")
        def static_files(filename):
            return send_from_directory(WEB_DIR, filename)

        @app.route("/api/status")
        def api_status():
            info = {}
            if "detector" in refs:
                info["platform"] = refs["detector"].get_info()
            if "brain" in refs:
                info["memory"] = refs["brain"].get_stats()
            info["modules"] = list(refs.keys())
            info["server_time"] = datetime.now().isoformat()
            return jsonify(info)

        @app.route("/api/command", methods=["POST"])
        def api_command():
            data = request.get_json(silent=True) or {}
            cmd = data.get("command", "")
            if not cmd:
                return jsonify({"error": "Comando vacío"}), 400
            if "brain" in refs:
                refs["brain"].record_conversation(f"[WEB] {cmd}", "Comando recibido")
            processor = refs.get("processor")
            if processor:
                result = processor(cmd)
                return jsonify({"command": cmd, "result": result})
            return jsonify({"command": cmd, "result": "Comando recibido"})

        @app.route("/api/memory", methods=["GET"])
        def api_memory():
            if "brain" not in refs:
                return jsonify({"error": "Módulo de aprendizaje no disponible"}), 503
            return jsonify(refs["brain"].list_all_facts() or {})

        @app.route("/api/memory", methods=["POST"])
        def api_memory_set():
            if "brain" not in refs:
                return jsonify({"error": "Módulo de aprendizaje no disponible"}), 503
            data = request.get_json(silent=True) or {}
            key = data.get("key")
            value = data.get("value")
            if key and value:
                refs["brain"].learn_fact(key, value)
                return jsonify({"status": "ok", "key": key, "value": value})
            return jsonify({"error": "key y value requeridos"}), 400

        @app.route("/api/conversations")
        def api_conversations():
            if "brain" not in refs:
                return jsonify([])
            return jsonify(refs["brain"]._memory.get("conversations", [])[-20:])

        @app.route("/api/platform")
        def api_platform():
            if "detector" in refs:
                return jsonify(refs["detector"].get_info())
            return jsonify({"platform": "desconocido"})

        @app.route("/api/knowledge/query", methods=["POST"])
        def api_knowledge_query():
            if "knowledge" not in refs:
                return jsonify({"error": "Motor de conocimiento no disponible"}), 503
            data = request.get_json(silent=True) or {}
            q = data.get("query", "")
            if not q:
                return jsonify({"error": "query requerida"}), 400
            results = refs["knowledge"].query(q)
            return jsonify({"query": q, "results": results})

        @app.route("/api/knowledge/absorb", methods=["POST"])
        def api_knowledge_absorb():
            if "knowledge" not in refs:
                return jsonify({"error": "Motor de conocimiento no disponible"}), 503
            data = request.get_json(silent=True) or {}
            text = data.get("text", "")
            source = data.get("source", "web")
            topic = data.get("topic", "general")
            if text:
                ok = refs["knowledge"].absorb_text(text, source=source, topic=topic)
                return jsonify({"absorbed": ok})
            url = data.get("url", "")
            if url:
                ok, msg = refs["knowledge"].absorb_url(url)
                return jsonify({"absorbed": ok, "message": msg})
            return jsonify({"error": "text o url requerido"}), 400

        @app.route("/api/knowledge/stats")
        def api_knowledge_stats():
            if "knowledge" not in refs:
                return jsonify({"error": "no disponible"}), 503
            return jsonify(refs["knowledge"].get_stats())

        @app.route("/api/knowledge/topics")
        def api_knowledge_topics():
            if "knowledge" not in refs:
                return jsonify([])
            return jsonify(refs["knowledge"].get_topics())

        @app.route("/api/knowledge/search", methods=["POST"])
        def api_knowledge_search():
            if "knowledge" not in refs:
                return jsonify({"error": "no disponible"}), 503
            data = request.get_json(silent=True) or {}
            topic = data.get("topic", "")
            if topic:
                return jsonify(refs["knowledge"].search_by_topic(topic))
            return jsonify(refs["knowledge"].search_by_source(data.get("source", "")))

        @app.route("/api/backends")
        def api_backends():
            if "knowledge" not in refs:
                return jsonify({})
            avail = refs["knowledge"].get_available_ai_backends()
            return jsonify(avail)

        @app.route("/api/code/detect", methods=["POST"])
        def api_code_detect():
            if "code_analyzer" not in refs:
                return jsonify({"error": "no disponible"}), 503
            data = request.get_json(silent=True) or {}
            codigo = data.get("code", "")
            if not codigo:
                return jsonify({"error": "code requerido"}), 400
            lang = refs["code_analyzer"].detectar_lenguaje(codigo)
            return jsonify({"lenguaje": lang})

        @app.route("/api/code/analyze", methods=["POST"])
        def api_code_analyze():
            if "code_analyzer" not in refs:
                return jsonify({"error": "no disponible"}), 503
            data = request.get_json(silent=True) or {}
            codigo = data.get("code", "")
            if not codigo:
                return jsonify({"error": "code requerido"}), 400
            res = refs["code_analyzer"].analizar(codigo)
            return jsonify(res)

        @app.route("/api/code/explain", methods=["POST"])
        def api_code_explain():
            if "code_analyzer" not in refs:
                return jsonify({"error": "no disponible"}), 503
            data = request.get_json(silent=True) or {}
            codigo = data.get("code", "")
            nivel = data.get("level", "simple")
            if not codigo:
                return jsonify({"error": "code requerido"}), 400
            res = refs["code_analyzer"].explicar(codigo, nivel=nivel)
            return jsonify(res)

        def run():
            app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def _start_stdlib(self):

        refs = self.jarvis_refs

        class JARVISHandler(BaseHTTPRequestHandler):

            def _send_json(self, data, status=200):
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

            def _send_html(self, html, status=200):
                self.send_response(status)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode())

            def _send_file(self, path):
                try:
                    with open(path, "rb") as f:
                        content = f.read()
                    ext = os.path.splitext(path)[1].lower()
                    types = {
                        ".html": "text/html",
                        ".css": "text/css",
                        ".js": "application/javascript",
                        ".png": "image/png",
                        ".jpg": "image/jpeg",
                        ".svg": "image/svg+xml",
                        ".ico": "image/x-icon",
                    }
                    self.send_response(200)
                    self.send_header("Content-Type", types.get(ext, "application/octet-stream"))
                    self.end_headers()
                    self.wfile.write(content)
                except FileNotFoundError:
                    self._send_html("<h1>404 Not Found</h1>", 404)

            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path

                if path == "/" or path == "/index.html":
                    self._send_file(os.path.join(WEB_DIR, "index.html"))
                elif path.startswith("/static/"):
                    filename = path[len("/static/"):]
                    self._send_file(os.path.join(WEB_DIR, filename))
                elif path == "/api/status":
                    info = {}
                    if "detector" in refs:
                        info["platform"] = refs["detector"].get_info()
                    if "brain" in refs:
                        info["memory"] = refs["brain"].get_stats()
                    info["server_time"] = datetime.now().isoformat()
                    self._send_json(info)
                elif path == "/api/platform":
                    if "detector" in refs:
                        self._send_json(refs["detector"].get_info())
                    else:
                        self._send_json({"platform": "desconocido"})
                elif path == "/api/memory":
                    if "brain" in refs:
                        facts = refs["brain"].list_all_facts()
                        self._send_json(facts if facts else {})
                    else:
                        self._send_json({"error": "no disponible"}, 503)
                elif path == "/api/conversations":
                    if "brain" in refs:
                        convos = refs["brain"]._memory.get("conversations", [])[-20:]
                        self._send_json(convos)
                    else:
                        self._send_json([])
                elif path == "/api/backends":
                    if "knowledge" in refs:
                        self._send_json(refs["knowledge"].get_available_ai_backends())
                    else:
                        self._send_json({})
                elif path == "/api/knowledge/stats":
                    if "knowledge" in refs:
                        self._send_json(refs["knowledge"].get_stats())
                    else:
                        self._send_json({"error": "no disponible"}, 503)
                elif path == "/api/knowledge/topics":
                    if "knowledge" in refs:
                        self._send_json(refs["knowledge"].get_topics())
                    else:
                        self._send_json([])
                else:
                    self._send_html("<h1>404 Not Found</h1>", 404)

            def do_POST(self):
                parsed = urllib.parse.urlparse(self.path)
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length) if content_length > 0 else b"{}"

                if parsed.path == "/api/command":
                    try:
                        data = json.loads(body)
                    except json.JSONDecodeError:
                        data = {}
                    cmd = data.get("command", "")
                    if "brain" in refs:
                        refs["brain"].record_conversation(f"[WEB] {cmd}", "Comando recibido")
                    processor = refs.get("processor")
                    if processor:
                        result = processor(cmd)
                        self._send_json({"command": cmd, "result": result})
                    else:
                        self._send_json({"command": cmd, "result": "Comando recibido"})

                elif parsed.path == "/api/memory":
                    try:
                        data = json.loads(body)
                    except json.JSONDecodeError:
                        data = {}
                    key = data.get("key")
                    value = data.get("value")
                    if key and value and "brain" in refs:
                        refs["brain"].learn_fact(key, value)
                        self._send_json({"status": "ok", "key": key, "value": value})
                    else:
                        self._send_json({"error": "key y value requeridos"}, 400)

                elif parsed.path == "/api/knowledge/query":
                    if "knowledge" not in refs:
                        self._send_json({"error": "no disponible"}, 503)
                    else:
                        try:
                            data = json.loads(body)
                        except json.JSONDecodeError:
                            data = {}
                        q = data.get("query", "")
                        if q:
                            results = refs["knowledge"].query(q)
                            self._send_json({"query": q, "results": results})
                        else:
                            self._send_json({"error": "query requerida"}, 400)

                elif parsed.path == "/api/knowledge/absorb":
                    if "knowledge" not in refs:
                        self._send_json({"error": "no disponible"}, 503)
                    else:
                        try:
                            data = json.loads(body)
                        except json.JSONDecodeError:
                            data = {}
                        text = data.get("text", "")
                        source = data.get("source", "web")
                        topic = data.get("topic", "general")
                        if text:
                            ok = refs["knowledge"].absorb_text(text, source=source, topic=topic)
                            self._send_json({"absorbed": ok})
                        else:
                            url = data.get("url", "")
                            if url:
                                ok, msg = refs["knowledge"].absorb_url(url)
                                self._send_json({"absorbed": ok, "message": msg})
                            else:
                                self._send_json({"error": "text o url requerido"}, 400)

                elif parsed.path == "/api/knowledge/search":
                    if "knowledge" not in refs:
                        self._send_json({"error": "no disponible"}, 503)
                    else:
                        try:
                            data = json.loads(body)
                        except json.JSONDecodeError:
                            data = {}
                        topic = data.get("topic", "")
                        if topic:
                            self._send_json(refs["knowledge"].search_by_topic(topic))
                        else:
                            self._send_json(refs["knowledge"].search_by_source(data.get("source", "")))

                elif parsed.path == "/api/code/detect":
                    if "code_analyzer" not in refs:
                        self._send_json({"error": "no disponible"}, 503)
                    else:
                        try:
                            data = json.loads(body)
                        except json.JSONDecodeError:
                            data = {}
                        codigo = data.get("code", "")
                        if codigo:
                            lang = refs["code_analyzer"].detectar_lenguaje(codigo)
                            self._send_json({"lenguaje": lang})
                        else:
                            self._send_json({"error": "code requerido"}, 400)

                elif parsed.path == "/api/code/analyze":
                    if "code_analyzer" not in refs:
                        self._send_json({"error": "no disponible"}, 503)
                    else:
                        try:
                            data = json.loads(body)
                        except json.JSONDecodeError:
                            data = {}
                        codigo = data.get("code", "")
                        if codigo:
                            res = refs["code_analyzer"].analizar(codigo)
                            self._send_json(res)
                        else:
                            self._send_json({"error": "code requerido"}, 400)

                elif parsed.path == "/api/code/explain":
                    if "code_analyzer" not in refs:
                        self._send_json({"error": "no disponible"}, 503)
                    else:
                        try:
                            data = json.loads(body)
                        except json.JSONDecodeError:
                            data = {}
                        codigo = data.get("code", "")
                        nivel = data.get("level", "simple")
                        if codigo:
                            res = refs["code_analyzer"].explicar(codigo, nivel=nivel)
                            self._send_json(res)
                        else:
                            self._send_json({"error": "code requerido"}, 400)

                else:
                    self._send_json({"error": "not found"}, 404)

            def log_message(self, format, *args):
                print(f"[WEB] {args[0]} {args[1]} {args[2]}")

        def run():
            server = HTTPServer((self.host, self.port), JARVISHandler)
            self._server = server
            server.serve_forever()

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    @safe_method
    def stop(self):

        self._running = False
        if self._server:
            self._server.shutdown()
            print("[WEB] Servidor detenido.")

    @safe_method
    def get_url(self):

        import socket
        hostname = socket.gethostbyname(socket.gethostname())
        return f"http://{hostname}:{self.port}"
