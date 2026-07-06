import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from CORE_SHARED.service_discovery import resolve, call_service
from JOSAMICK.security_guard import security_guard
from JOSAMICK.mesh_protocol import start_heartbeat, mesh_handshake, command_executor

if __name__ == "__main__":
    print("[BRAIN CORE] Iniciando cerebro de IA...")
    handshake = mesh_handshake()
    if handshake.get("ok"):
        print(f"[BRAIN] Handshake exitoso - Rol: {handshake.get('assigned_function','unknown')}")
    else:
        print(f"[BRAIN] Handshake diferido: {handshake}")
    start_heartbeat()
    print("[BRAIN Core] Heartbeat iniciado (cada 30s)")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[BRAIN] Detenido.")
