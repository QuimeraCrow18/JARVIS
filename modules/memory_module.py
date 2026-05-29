# ==========================================
# MEMORY MANAGER
# modules/memory_module.py
# ==========================================

import os
import gc
import psutil

from core.utils import safe_method  # Importa el decorador

class MemoryManager:

    def __init__(self):
        print("[MEMORY] Memory Manager iniciado.")

    # ==========================================
    # OBTENER USO DE RAM
    # ==========================================
    @safe_method
    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        used = ram.percent
        print(f"[MEMORY] RAM usada: {used}%")
        return used

    # ==========================================
    # OPTIMIZAR MEMORIA
    # ==========================================
    @safe_method
    def optimize_memory(self):
        print("[MEMORY] Limpiando memoria...")
        gc.collect()
        os.system("ipconfig /flushdns")
        return True

    # ==========================================
    # ESTADO GENERAL
    # ==========================================
    @safe_method
    def system_status(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        status = {
            "cpu": cpu,
            "ram": ram,
            "disk": disk
        }
        print(f"[STATUS] CPU: {cpu}%")
        print(f"[STATUS] RAM: {ram}%")
        print(f"[STATUS] DISCO: {disk}%")
        return status