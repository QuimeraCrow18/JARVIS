# ==========================================
# AUTOMATION MODULE
# modules/automation_module.py
# ==========================================

import os
import time
import subprocess
import webbrowser
import glob


class AutomationModule:

    def __init__(self):

        print("[AUTOMATION] Módulo cargado.")

    # ==========================================
    # ABRIR APLICACIÓN POR RUTA
    # ==========================================

    def open_app(self, app_name):

        try:

            app_name = app_name.lower()

            print(f"[AUTOMATION] Abriendo: {app_name}")

            # ======================================
            # BRAVE
            # ======================================

            if "brave" in app_name:

                os.system("start brave")
                return True

            # ======================================
            # GOOGLE CHROME
            # ======================================

            elif "chrome" in app_name:

                os.system("start chrome")
                return True

            # ======================================
            # FIREFOX
            # ======================================

            elif "firefox" in app_name:

                os.system("start firefox")
                return True

            # ======================================
            # EDGE
            # ======================================

            elif "edge" in app_name:

                os.system("start msedge")
                return True

            # ======================================
            # CALCULADORA
            # ======================================

            elif "calculadora" in app_name:

                os.system("start calc")
                return True

            # ======================================
            # BLOC DE NOTAS
            # ======================================

            elif "notas" in app_name:

                os.system("start notepad")
                return True

            # ======================================
            # EXPLORADOR
            # ======================================

            elif "explorador" in app_name:

                os.system("start explorer")
                return True

            # ======================================
            # VISUAL STUDIO CODE
            # ======================================

            elif "visual studio" in app_name or "vs code" in app_name:

                os.system("start code")
                return True

            # ======================================
            # PANEL DE CONTROL
            # ======================================

            elif "panel de control" in app_name:

                os.system("control")
                return True

            # ======================================
            # CONFIGURACIÓN
            # ======================================

            elif "configuración" in app_name:

                os.system("start ms-settings:")
                return True

            # ======================================
            # ADMINISTRADOR DE TAREAS
            # ======================================

            elif "administrador de tareas" in app_name:

                os.system("start taskmgr")
                return True

            # ======================================
            # CMD
            # ======================================

            elif "cmd" in app_name:

                os.system("start cmd")
                return True

            # ======================================
            # POWERSHELL
            # ======================================

            elif "powershell" in app_name:

                os.system("start powershell")
                return True

            # ======================================
            # REPRODUCTOR
            # ======================================

            elif "reproductor" in app_name:

                os.system("start wmplayer")
                return True

            # ======================================
            # WORD
            # ======================================

            elif "word" in app_name:

                os.system("start winword")
                return True

            # ======================================
            # EXCEL
            # ======================================

            elif "excel" in app_name:

                os.system("start excel")
                return True

            # ======================================
            # POWERPOINT
            # ======================================

            elif "powerpoint" in app_name:

                os.system("start powerpnt")
                return True

            else:

                print("[AUTOMATION] Aplicación no reconocida.")
                return False

        except Exception as e:

            print("[AUTOMATION ERROR]", e)
            return False

    # ==========================================
    # ABRIR SITIO WEB
    # ==========================================

    def open_website(self, url):

        try:

            print(f"[WEB] Abriendo: {url}")

            webbrowser.open(url)

            return True

        except Exception as e:

            print("[WEB ERROR]", e)
            return False

    # ==========================================
    # BUSCAR ARCHIVOS
    # ==========================================

    def search_file(self, filename):

        try:

            print(f"[SEARCH] Buscando: {filename}")

            search_paths = [
                "C:\\Users",
                "D:\\"
            ]

            for path in search_paths:

                files = glob.glob(
                    f"{path}/**/*{filename}*",
                    recursive=True
                )

                if files:

                    print(f"[SEARCH] Encontrado: {files[0]}")

                    return files[0]

            print("[SEARCH] Archivo no encontrado.")

            return None

        except Exception as e:

            print("[SEARCH ERROR]", e)
            return None

    # ==========================================
    # ABRIR ARCHIVO
    # ==========================================

    def open_file(self, filepath):

        try:

            print(f"[FILE] Abriendo: {filepath}")

            os.startfile(filepath)

            return True

        except Exception as e:

            print("[FILE ERROR]", e)
            return False

    # ==========================================
    # APAGAR PC
    # ==========================================

    def shutdown_pc(self):

        try:

            print("[SYSTEM] Apagando PC...")

            os.system("shutdown /s /t 5")

            return True

        except Exception as e:

            print("[SHUTDOWN ERROR]", e)
            return False

    # ==========================================
    # REINICIAR PC
    # ==========================================

    def restart_pc(self):

        try:

            print("[SYSTEM] Reiniciando PC...")

            os.system("shutdown /r /t 5")

            return True

        except Exception as e:

            print("[RESTART ERROR]", e)
            return False

    # ==========================================
    # BLOQUEAR PC
    # ==========================================

    def lock_pc(self):

        try:

            print("[SYSTEM] Bloqueando PC...")

            os.system(
                "rundll32.exe user32.dll,LockWorkStation"
            )

            return True

        except Exception as e:

            print("[LOCK ERROR]", e)
            return False