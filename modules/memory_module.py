# ==========================================
# MEMORY MANAGER
# modules/memory_manager.py
# ==========================================

import os
import gc
import psutil


class MemoryManager:

    def __init__(self):

        print("[MEMORY] Memory Manager iniciado.")

    # ==========================================
    # OBTENER USO DE RAM
    # ==========================================

    def get_ram_usage(self):

        try:

            ram = psutil.virtual_memory()

            used = ram.percent

            print(f"[MEMORY] RAM usada: {used}%")

            return used

        except Exception as e:

            print("[MEMORY ERROR]", e)
            return 0

    # ==========================================
    # OPTIMIZAR MEMORIA
    # ==========================================

    def optimize_memory(self):

        try:

            print("[MEMORY] Limpiando memoria...")

            gc.collect()

            os.system("ipconfig /flushdns")

            return True

        except Exception as e:

            print("[OPTIMIZE ERROR]", e)
            return False

    # ==========================================
    # ESTADO GENERAL
    # ==========================================

    def system_status(self):

        try:

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

        except Exception as e:

            print("[STATUS ERROR]", e)

            return {

                "cpu": 0,
                "ram": 0,
                "disk": 0

            }