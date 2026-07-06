import os
import json
import time
import threading
import urllib.request
import urllib.error

SERVICES = {}
_SERVICES_LOCK = threading.Lock()
_CIRCUIT_STATES = {}
_CB_LOCK = threading.Lock()

def _load_env_services():
    return {
        "cerebro": os.getenv("JOSAMICK_SERVICE", "cerebro:5001"),
        "gateway": os.getenv("KEXPLER_SERVICE", "gateway:5002"),
        "c2": os.getenv("C2_SERVICE", "c2:9090"),
        "discovery": os.getenv("SERVICE_DISCOVERY_URL", "http://discovery:8500"),
    }

def _parse_addr(addr):
    parts = addr.split(":")
    host = parts[0]
    port = int(parts[1]) if len(parts) > 1 else 80
    return host, port

def resolve(service_name):
    with _SERVICES_LOCK:
        if service_name in SERVICES:
            return SERVICES[service_name]
        services = _load_env_services()
        if service_name in services:
            host, port = _parse_addr(services[service_name])
            entry = {"host": host, "port": port, "url": f"http://{host}:{port}"}
            SERVICES[service_name] = entry
            return entry
    return None

def discover_all():
    services = _load_env_services()
    with _SERVICES_LOCK:
        for name, addr in services.items():
            host, port = _parse_addr(addr)
            SERVICES[name] = {"host": host, "port": port, "url": f"http://host}:{port}"}

class CircuitBreaker:
    def __init__(self, name, timeout=None, max_retries=None, recovery_interval=None):
        self.name = name
        self.timeout = timeout or int(os.getenv("CB_TIMEOUT", "5"))
        self.max_retries = max_retries or int(os.getenv("CB_MAX_RETRIES", "3"))
        self.recovery_interval = recovery_interval or int(os.getenv("CB_RECOVERY_INTERVAL", "30"))
        self._fail_count = 0
        self._state = "CLOSED"
        self._last_failure = 0

    def call(self, method, path, body=None, headers=None):
        svc = resolve(self.name)
        if not svc:
            return {"error": f"service_{self.name}_not_found", "_circuit": "OPEN", "_available": False}
        with _CB_LOCK:
            if self._state == "OPEN":
                if time.time() - self._last_failure >= self.recovery_interval:
                    self._state = "HALF_OPEN"
                else:
                    return {"error": f"circuit_open_{self.name}", "_circuit": "OPEN", "_available": False}
        url = f"{svc['url']}{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                resp = json.loads(r.read().decode())
                with _CB_LOCK:
                    self._fail_count = 0
                    self._state = "CLOSED"
                resp["_circuit"] = "CLOSED"
                resp["_available"] = True
                return resp
        except Exception as e:
            with _CB_LOCK:
                self._fail_count += 1
                self._last_failure = time.time()
                if self._fail_count >= self.max_retries:
                    self._state = "OPEN"
            return {
                "error": str(e),
                "_circuit": self._state,
                "_available": False,
                "_service": self.name
            }

def get_circuit(name):
    return CircuitBreaker(name)

def call_service(service_name, method="GET", path="/", body=None, headers=None):
    cb = get_circuit(service_name)
    return cb.call(method, path, body, headers)
