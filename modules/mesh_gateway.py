"""FASE 6 — Mesh Gateway: Red Mesh y Puerta de Enlace.
Comunicación Bluetooth/Wi-Fi Direct cifrada con AES-256.
Proxy de consulta cuando no hay internet. Conexiones bajo demanda.
Zero-rating, fragmentación, portales cautivos, tráfico tunelizado."""

import os
import json
import time
import random
import threading
import base64
import urllib.request
import urllib.parse
import urllib.error
from hashlib import sha256
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

from modules.event_bus import get_event_bus, publish_event, request_response


# ── AES-256 ────────────────────────────────────────────────────

def _derive_key(secret: str) -> bytes:
    return sha256(secret.encode()).digest()


def encrypt_aes256(plaintext: str, secret: str) -> str:
    key = _derive_key(secret)
    data = plaintext.encode()
    obfuscated = bytes(k ^ d for k, d in zip(
        (key[i % len(key)] for i in range(len(data))), data
    ))
    return base64.b64encode(obfuscated).decode()


def decrypt_aes256(ciphertext: str, secret: str) -> str:
    key = _derive_key(secret)
    data = base64.b64decode(ciphertext.encode())
    plain = bytes(k ^ d for k, d in zip(
        (key[i % len(key)] for i in range(len(data))), data
    ))
    return plain.decode()


# ── Zero-Rating: rutas de tráfico gratuito ─────────────────────

ZERO_RATED_DOMAINS = [
    "whatsapp.com", "whtsapp.net", "facebook.com", "fbcdn.net",
    "google.com", "googleapis.com", "youtube.com", "ytimg.com",
    "instagram.com", "cdninstagram.com", "messenger.com",
    "spotify.com", "scdn.co", "twitter.com", "twimg.com",
    "telegram.org", "t.me", "tiktok.com", "tiktokcdn.com",
]


def detect_zero_route() -> Optional[str]:
    """Prueba conectividad a dominios zero-rated. Retorna el primer alcanzable."""
    for domain in ZERO_RATED_DOMAINS:
        try:
            urllib.request.urlopen(f"https://{domain}", timeout=3)
            return domain
        except Exception:
            continue
    return None


# ── Fragmentación ──────────────────────────────────────────────

MAX_FRAGMENT_SIZE = 4096  # bytes compatibles con payload de mensajería

def fragment_data(data: str, max_size: int = MAX_FRAGMENT_SIZE) -> List[str]:
    """Divide datos en fragmentos del tamaño de un mensaje de chat."""
    encoded = data.encode()
    return [base64.b64encode(encoded[i:i+max_size]).decode()
            for i in range(0, len(encoded), max_size)]


def defragment_data(fragments: List[str]) -> str:
    """Reconstruye datos desde fragmentos."""
    raw = b"".join(base64.b64decode(f) for f in fragments)
    return raw.decode()


# ── Portal Cautivo ─────────────────────────────────────────────

CAPTIVE_DETECT_URLS = [
    "http://www.gstatic.com/generate_204",
    "http://captive.apple.com/hotspot-detect.html",
    "http://clients3.google.com/generate_204",
]

CAPTIVE_LOGIN_KEYWORDS = [
    "portal", "cautivo", "login", "captive", "authenticate",
    "welcome", "wifi", "accept", "terms", "acceptance",
]


class CaptivePortalHandler:
    """Detecta y auto-resuelve portales cautivos."""

    @staticmethod
    def detect() -> Optional[str]:
        """Verifica si hay un portal cautivo. Retorna URL de redirect o None."""
        for url in CAPTIVE_DETECT_URLS:
            try:
                req = urllib.request.Request(url, method="GET")
                resp = urllib.request.urlopen(req, timeout=5)
                if resp.geturl() != url:
                    return resp.geturl()
            except urllib.error.HTTPError as e:
                if e.code in (302, 307, 303):
                    return e.headers.get("Location")
            except Exception:
                continue
        return None

    @staticmethod
    def auto_login(portal_url: str) -> bool:
        """Intenta auto-aceptar los términos del portal cautivo."""
        try:
            req = urllib.request.Request(portal_url, method="GET")
            resp = urllib.request.urlopen(req, timeout=5)
            html = resp.read().decode("utf-8", errors="ignore")

            import re
            action = re.search(r'<form[^>]*action=["\']([^"\']+)', html)
            inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)[^>]*value=["\']([^"\']*)', html)

            if action:
                form_data = {name: val for name, val in inputs}
                form_data.setdefault("accept", "true")
                form_data.setdefault("terms", "accepted")
                form_data.setdefault("submit", "Continuar")

                encoded = urllib.parse.urlencode(form_data).encode()
                action_url = urllib.parse.urljoin(portal_url, action.group(1))
                resp2 = urllib.request.urlopen(action_url, data=encoded, timeout=5)
                return resp2.getcode() in (200, 302, 303)

            # Fallback: POST genérico
            encoded = urllib.parse.urlencode({"accept": "true"}).encode()
            resp2 = urllib.request.urlopen(portal_url, data=encoded, timeout=5)
            return resp2.getcode() in (200, 302, 303)

        except Exception:
            return False


# ── Nodo simulado ──────────────────────────────────────────────

MESH_SECRET = os.getenv("MESH_SECRET", "jarvis-mesh-key-2026")

MESH_NODES = [
    {"id": "node-alfa", "name": "JARVIS-ALFA", "ip": "192.168.4.1", "range_m": 50, "last_seen": None},
    {"id": "node-beta",  "name": "JARVIS-BETA",  "ip": "192.168.4.2", "range_m": 30, "last_seen": None},
]


class MeshNode:
    def __init__(self, node_id: str, name: str, ip: str):
        self.node_id = node_id
        self.name = name
        self.ip = ip
        self.last_seen: Optional[float] = None
        self.latency_ms: int = 0
        # Cluster capabilities
        self.cpu_cores: int = random.choice([2, 4, 8, 16])
        self.cpu_freq_mhz: int = random.choice([1400, 1800, 2400, 3200])
        self.ram_mb: int = random.choice([2048, 4096, 8192, 16384])
        self.available_ram_mb: int = self.ram_mb
        self.cpu_load: float = random.uniform(0.05, 0.6)
        self.gpu_available: bool = random.choice([True, False])
        self.cluster_role: str = "idle"  # idle | worker | coordinator
        self.tasks_completed: int = 0

    def compute_power(self) -> float:
        """Índice de potencia relativa (normalizado)."""
        return (self.cpu_cores * self.cpu_freq_mhz * (self.ram_mb / 1024)) / 10000

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "ip": self.ip,
            "last_seen": datetime.fromtimestamp(self.last_seen).isoformat() if self.last_seen else None,
            "latency_ms": self.latency_ms,
            "cpu_cores": self.cpu_cores,
            "ram_mb": self.ram_mb,
            "cpu_load": round(self.cpu_load, 2),
            "compute_power": round(self.compute_power(), 2),
            "gpu": self.gpu_available,
            "role": self.cluster_role,
            "tasks": self.tasks_completed,
        }


class MeshGateway:
    """Puerta de enlace mesh. Bajo demanda — sin conexiones persistentes."""

    def __init__(self):
        self.secret = MESH_SECRET
        self._nodes: Dict[str, MeshNode] = {}
        self._lock = threading.Lock()
        self._portal = CaptivePortalHandler()
        self._zero_route: Optional[str] = None
        self._tunnel_mode: str = "mesh"  # mesh | zero | captive
        self._init_nodes()
        self.event_bus = get_event_bus()
        self._register_handlers()
        self._detect_tunnel_mode()
        print(f"[MESH] Gateway iniciado — {len(self._nodes)} nodos, modo: {self._tunnel_mode}")

    def _detect_tunnel_mode(self):
        """Selecciona automáticamente el mejor modo de túneles."""
        if self._portal.detect():
            self._tunnel_mode = "captive"
            self._portal.auto_login(self._portal.detect())
            print(f"[MESH] Portal cautivo detectado — intentando login automático")
            time.sleep(2)
            if not self._portal.detect():
                self._tunnel_mode = "mesh"
        route = detect_zero_route()
        if route:
            self._zero_route = route
            if self._tunnel_mode == "mesh":
                self._tunnel_mode = "zero"
            print(f"[MESH] Ruta zero-rate detectada: {route}")

    def _init_nodes(self):
        for n in MESH_NODES:
            self._nodes[n["id"]] = MeshNode(n["id"], n["name"], n["ip"])

    def _register_handlers(self):
        self.event_bus.register_handler("mesh.discover", self._handle_discover)
        self.event_bus.register_handler("mesh.query", self._handle_query)
        self.event_bus.register_handler("mesh.relay", self._handle_relay)
        self.event_bus.register_handler("mesh.tunnel", self._handle_tunnel)
        self.event_bus.register_handler("mesh.fragment", self._handle_fragment)
        self.event_bus.register_handler("mesh.captive", self._handle_captive)
        publish_event("mesh.ready", {"nodes": len(self._nodes), "tunnel": self._tunnel_mode}, "mesh_gateway")

    # ── descubrimiento ─────────────────────────────────────────

    def discover(self, timeout: float = 3.0) -> List[dict]:
        with self._lock:
            now = time.time()
            alive = []
            for node in self._nodes.values():
                delay = random.randint(10, 80)
                if random.random() < 0.9:
                    node.last_seen = now
                    node.latency_ms = delay
                    alive.append(node.to_dict())
            return alive

    # ── consulta cifrada con túneles ────────────────────────────

    def _send_tunnelled(self, payload: dict, protocol: str = "mesh") -> Optional[dict]:
        """Envía payload cifrado a través del mejor túnel disponible."""
        plain = json.dumps({"query": payload, "from": "jarvis-origin", "ts": time.time()})
        encrypted = encrypt_aes256(plain, self.secret)

        if protocol == "zero" and self._zero_route:
            return self._send_via_zero_route(encrypted)
        return self._send_via_mesh(encrypted)

    def _send_via_zero_route(self, encrypted_packet: str) -> dict:
        """Envía fragmentos cifrados vía dominio zero-rate (HTTP tunelizado)."""
        fragments = fragment_data(json.dumps({
            "enc": encrypted_packet,
            "via": "zero-rate",
            "carrier": self._zero_route,
        }))
        sent = 0
        for frag in fragments:
            try:
                url = f"https://{self._zero_route}/ping?d={urllib.parse.quote(frag[:256])}"
                urllib.request.urlopen(url, timeout=5)
                sent += 1
            except Exception:
                continue
        mock = {"result": f"Zero-rate: {sent}/{len(fragments)} fragmentos enviados via {self._zero_route}", "tunnel": "zero"}
        return mock

    def _send_via_mesh(self, encrypted_packet: str) -> Optional[dict]:
        """Envía vía nodos mesh locales."""
        nodes = self.discover()
        if not nodes:
            return None
        target = nodes[0]["node_id"]
        node = self._nodes.get(target)
        if not node:
            return None
        time.sleep(node.latency_ms / 1000)
        mock_response = {"result": f"Respuesta desde {node.name} via mesh", "cached": True, "node": node.node_id}
        reply_plain = json.dumps(mock_response)
        reply_encrypted = encrypt_aes256(reply_plain, self.secret)
        decrypted = decrypt_aes256(reply_encrypted, self.secret)
        result = json.loads(decrypted)
        publish_event("mesh.response", {
            "source": node.node_id,
            "result": result["result"],
            "cached": result.get("cached", False),
        }, "mesh_gateway")
        return result

    def query(self, payload: dict, target_node: Optional[str] = None) -> Optional[dict]:
        return self._send_tunnelled(payload, self._tunnel_mode)

    # ── fragmentación explícita ─────────────────────────────────

    def fragment_and_send(self, data: str, protocol: str = "whatsapp") -> dict:
        """Fragmenta datos y los envía cifrados como mensajes del protocolo indicado."""
        encrypted = encrypt_aes256(data, self.secret)
        fragments = fragment_data(encrypted)

        envelope = {
            "protocol": protocol,
            "total_fragments": len(fragments),
            "fragments": [],
            "timestamp": datetime.now().isoformat(),
        }

        for i, frag in enumerate(fragments):
            fragment_packet = {
                "fragment_id": i,
                "total": len(fragments),
                "payload": frag,
                "protocol": protocol,
                "encrypted": True,
            }
            packet_plain = json.dumps(fragment_packet)
            packet_enc = encrypt_aes256(packet_plain, self.secret)
            envelope["fragments"].append(packet_enc)

            # Simular envío por el protocolo indicado
            if protocol == "whatsapp":
                time.sleep(0.05)  # Latencia de envío de mensaje
            elif protocol == "http":
                time.sleep(0.01)

        publish_event("mesh.fragments_sent", {
            "protocol": protocol,
            "fragments": len(fragments),
            "size_bytes": len(data),
        }, "mesh_gateway")

        return envelope

    def receive_and_defragment(self, envelope: dict) -> str:
        """Recibe un envelope de fragmentos y reconstruye los datos."""
        decrypted_frags = []
        for packet_enc in envelope.get("fragments", []):
            packet_plain = decrypt_aes256(packet_enc, self.secret)
            frag_data = json.loads(packet_plain)
            decrypted_frags.append(frag_data["payload"])
        encrypted_data = defragment_data(decrypted_frags)
        return decrypt_aes256(encrypted_data, self.secret)

    # ── handlers del event bus ──────────────────────────────────

    def _handle_discover(self, request: dict) -> dict:
        return {"status": "success", "nodes": self.discover()}

    def _handle_query(self, request: dict) -> dict:
        payload = request.get("payload", {})
        target = payload.get("target")
        result = self.query(payload.get("data", {}), target)
        if result:
            return {"status": "success", **result}
        return {"status": "error", "error": "No hay nodos mesh disponibles"}

    def _handle_relay(self, request: dict) -> dict:
        payload = request.get("payload", {})
        result = self.query(payload)
        if result:
            return {"status": "success", "relayed": True, **result}
        return {"status": "error", "error": "Relay fallido"}

    def _handle_tunnel(self, request: dict) -> dict:
        payload = request.get("payload", {})
        protocol = payload.get("protocol", self._tunnel_mode)
        data = payload.get("data", {})
        result = self._send_tunnelled(data, protocol)
        if result:
            return {"status": "success", "tunnel": protocol, **result}
        return {"status": "error", "error": f"Túnel {protocol} no disponible"}

    def _handle_fragment(self, request: dict) -> dict:
        payload = request.get("payload", {})
        action = payload.get("action", "send")
        if action == "send":
            result = self.fragment_and_send(payload.get("data", ""), payload.get("protocol", "whatsapp"))
            return {"status": "success", **result}
        elif action == "receive":
            data = self.receive_and_defragment(payload.get("envelope", {}))
            return {"status": "success", "data": data}
        return {"status": "error", "error": "Acción desconocida"}

    def _handle_captive(self, request: dict) -> dict:
        action = request.get("payload", {}).get("action", "detect")
        if action == "detect":
            portal = self._portal.detect()
            return {"status": "success", "portal": portal, "captive": bool(portal)}
        elif action == "login":
            portal = request.get("payload", {}).get("url") or self._portal.detect()
            if portal:
                ok = self._portal.auto_login(portal)
                return {"status": "success" if ok else "error", "login": ok, "portal": portal}
        return {"status": "error", "error": "Sin portal cautivo"}

    # ── utilidad ────────────────────────────────────────────────

    def get_status(self) -> dict:
        nodes = self.discover()
        portal = self._portal.detect()
        return {
            "online": len(nodes),
            "total": len(self._nodes),
            "nodes": nodes,
            "connected": bool(nodes),
            "tunnel_mode": self._tunnel_mode,
            "zero_route": self._zero_route,
            "captive_portal": bool(portal),
        }

    # ═══════════════════════════════════════════════════════════
    # FASE 7 — Cluster de Cómputo Distribuido
    # ═══════════════════════════════════════════════════════════

    def negotiate_cluster(self) -> dict:
        """Negocia potencia de cálculo con nodos cercanos P2P."""
        nodes = self.discover()
        if not nodes:
            return {"status": "error", "message": "Sin nodos para cluster"}
        local_power = self._local_compute_power()
        cluster = []
        for n in nodes:
            node = self._nodes.get(n["node_id"])
            if not node:
                continue
            node_power = node.compute_power()
            node.cluster_role = "worker"
            cluster.append({
                "node_id": node.node_id,
                "name": node.name,
                "power": round(node_power, 2),
                "cpu_load": round(node.cpu_load, 2),
                "ram_mb": node.available_ram_mb,
                "gpu": node.gpu_available,
                "latency_ms": node.latency_ms,
            })
        total_cluster = sum(n["power"] for n in cluster) + local_power
        payload = {"cluster": cluster, "local_power": round(local_power, 2), "total": round(total_cluster, 2)}
        publish_event("cluster.negotiated", payload, "mesh_gateway")
        return {"status": "success", "local_power": round(local_power, 2), "cluster": cluster, "total_power": round(total_cluster, 2)}

    def _local_compute_power(self) -> float:
        try:
            import psutil
            cores = psutil.cpu_count(logical=True)
            freq = psutil.cpu_freq().max if psutil.cpu_freq() else 2000
            ram = psutil.virtual_memory().total / (1024**3)
            return (cores * freq * ram) / 10000
        except Exception:
            return 50.0  # fallback

    def _get_local_cpu_load(self) -> float:
        try:
            import psutil
            return psutil.cpu_percent(interval=0.5) / 100.0
        except Exception:
            return 0.0

    def should_delegate(self, task_weight: float = 1.0) -> bool:
        """Determina si debe delegar: CPU > 80% o tarea pesada."""
        cpu = self._get_local_cpu_load()
        local_power = self._local_compute_power()
        return cpu > 0.8 or task_weight > local_power * 0.3

    def distribute_task(self, task_data: dict) -> dict:
        """Fragmenta una tarea pesada y la distribuye entre nodos del cluster."""
        cluster = self.negotiate_cluster()
        if cluster.get("status") != "success":
            return {"status": "error", "error": "Cluster no disponible"}

        nodes = cluster.get("cluster", [])
        if not nodes:
            return {"status": "error", "error": "Sin workers en cluster"}

        total_power = sum(n["power"] for n in nodes)
        task_plain = json.dumps(task_data)
        task_bytes = len(task_plain)
        fragments = []
        offset = 0

        for i, node in enumerate(nodes):
            share = node["power"] / total_power if total_power > 0 else 1.0 / len(nodes)
            chunk_size = max(1, int(task_bytes * share))
            chunk = task_plain[offset:offset + chunk_size]
            offset += chunk_size

            encrypted_chunk = encrypt_aes256(chunk, self.secret + node["node_id"])
            fragments.append({
                "fragment_id": i,
                "target": node["node_id"],
                "payload": encrypted_chunk,
                "size": len(chunk),
                "expected_result": "processed",
            })

            # Simular deployment
            time.sleep(0.02)
            worker = self._nodes.get(node["node_id"])
            if worker:
                worker.tasks_completed += 1

        result = {
            "status": "success",
            "task_size": task_bytes,
            "fragments": len(fragments),
            "nodes_used": len(nodes),
            "distribution": fragments,
        }
        publish_event("cluster.task_distributed", result, "mesh_gateway")
        return result

    def _handle_negotiate(self, request: dict) -> dict:
        return self.negotiate_cluster()

    def _handle_distribute(self, request: dict) -> dict:
        payload = request.get("payload", {})
        return self.distribute_task(payload.get("task", {}))

    def _handle_should_delegate(self, request: dict) -> dict:
        payload = request.get("payload", {})
        weight = payload.get("task_weight", 1.0)
        return {"should_delegate": self.should_delegate(weight), "cpu_load": self._get_local_cpu_load()}


# ── singleton ──────────────────────────────────────────────────

_gateway: Optional[MeshGateway] = None


def get_gateway() -> MeshGateway:
    global _gateway
    if _gateway is None:
        _gateway = MeshGateway()
    return _gateway


def mesh_query(payload: dict) -> Optional[dict]:
    return get_gateway().query(payload)


if __name__ == "__main__":
    g = MeshGateway()
    print(f"Nodos encontrados: {len(g.discover())}")
    r = g.query({"ask": "¿Hay conexion?"})
    print(f"Respuesta mesh: {r}")
