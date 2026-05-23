# ==========================================
# SYSTEM MODULE
# modules/system_module.py
# ==========================================

import os
import platform
import psutil

class SystemModule:

    def shutdown(self):
        print("[SYSTEM] Apagando equipo")
        os.system("shutdown /s /t 1")

    def restart(self):
        print("[SYSTEM] Reiniciando equipo")
        os.system("shutdown /r /t 1")

    def system_info(self):
        info = {
            "Sistema": platform.system(),
            "Versión": platform.version(),
            "Arquitectura": platform.architecture(),
            "CPU": platform.processor(),
            "RAM Total (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
        }
        print("[SYSTEM INFO]", info)
        return info

    def open_folder(self, path):
        try:
            print(f"[SYSTEM] Abriendo carpeta: {path}")
            os.startfile(path)
        except Exception as e:
            print("[SYSTEM ERROR]", e)