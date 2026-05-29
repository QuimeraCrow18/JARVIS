## === AUTOIMPORTS/REGISTRO AUTOMÁTICO DE MÓDULOS ===
import os
import sys
import subprocess
import time
import threading

def autoregistrar_modules_once():
    auto_script = os.path.join(os.path.dirname(__file__), "utils", "autoregistrar.py")
    # Checa si el script se ha corrido "recientemente" (10 segundos) y si no, lo ejecuta.
    # Así no corre dos veces si main.py importa otros scripts.
    flag_file = os.path.join(os.path.dirname(__file__), ".modules_autoreg_flag")
    t = time.time()
    if os.path.exists(flag_file):
        last_exec = os.path.getmtime(flag_file)
        if t - last_exec < 10:
            return
    try:
        subprocess.run([sys.executable, auto_script], check=True)
        with open(flag_file, "w") as f:
            f.write(str(t))
    except Exception as e:
        print(f"[MODULAR-AUTOREG] Falló el autoregistro de módulos: {e}")

autoregistrar_modules_once()
# === FIN DE AUTOIMPORTS/REGISTRO ===

# === GIT AUTO-SYNC (SINCRONIZACIÓN AUTOMÁTICA CON GITHUB) ===
def start_git_auto_sync():
    try:
        auto_sync_script = os.path.join(os.path.dirname(__file__), "utils", "git_auto_sync.py")
        sync_thread = threading.Thread(
            target=lambda: subprocess.run([sys.executable, auto_sync_script]),
            daemon=True
        )
        sync_thread.start()
        print("[GIT-AUTO-SYNC] Sincronización automática con GitHub iniciada")
    except Exception as e:
        print(f"[GIT-AUTO-SYNC] No se pudo iniciar: {e}")

start_git_auto_sync()
# === FIN GIT AUTO-SYNC ===

# ==========================================
# JARVIS CORE SYSTEM
# ==========================================

from core.auto_repair import AutoRepair
from core.safe_loader import SafeLoader
from core.logger import JarvisLogger
from core.error_manager import ErrorManager

# ==========================================
# LOGGER
# ==========================================

logger = JarvisLogger()

logger.info("=================================")
logger.info("INICIANDO JARVIS")
logger.info("=================================")

# ==========================================
# ERROR MANAGER
# ==========================================

error_manager = ErrorManager()

# ==========================================
# AUTO REPAIR SYSTEM
# ==========================================

logger.info("Iniciando sistema AutoRepair...")

repair = AutoRepair()

repair.check_dependencies()

logger.info("AutoRepair finalizado.")

# ==========================================
# SAFE MODULE LOADER
# ==========================================

logger.info("Cargando módulos seguros...")

loader = SafeLoader()

# ==========================================
# SAFE IMPORTS
# ==========================================

voice_module = loader.load_module("voice.voice")

media_module = loader.load_module(
    "modules.media_module"
)

enhance_module = loader.load_module(
    "modules.enhance_module"
)

automation_module = loader.load_module(
    "modules.automation_module"
)

memory_module = loader.load_module(
    "modules.memory_module"
)

render_module = loader.load_module(
    "ui.render_panel"
)

faces_panel_module = loader.load_module(
    "ui.faces_panel"
)

# ==========================================
# MODULE STATUS
# ==========================================

loaded_modules = {
    "voice": voice_module,
    "media": media_module,
    "enhance": enhance_module,
    "automation": automation_module,
    "memory": memory_module,
    "render": render_module,
    "faces_panel": faces_panel_module
}

logger.info("Verificando módulos cargados...")

for module_name, module_data in loaded_modules.items():

    if module_data:

        logger.info(
            f"[OK] {module_name}"
        )

    else:

        logger.warning(
            f"[DESACTIVADO] {module_name}"
        )

# ==========================================
# BOOT SCREEN
# ==========================================

print("""

=========================================
            JARVIS ONLINE
=========================================

Sistema estable iniciado
AutoRepair activo
SafeLoader activo
Logs activos
Modo modular activo
Auto-Sync GitHub activo

=========================================

""")

logger.info("Jarvis iniciado correctamente.")

# ==========================================
# MAIN LOOP
# ==========================================

while True:

    try:

        command = input("Jarvis > ")

        # ==================================
        # SALIR
        # ==================================

        if command.lower() in [
            "salir",
            "exit",
            "cerrar",
            "apagar jarvis"
        ]:

            logger.info("Cerrando Jarvis...")

            print("Jarvis apagado.")

            break

        # ==================================
        # STATUS
        # ==================================

        elif command.lower() == "status":

            print("\n===== ESTADO DE MODULOS =====\n")

            for module_name, module_data in loaded_modules.items():

                if module_data:

                    print(f"[OK] {module_name}")

                else:

                    print(f"[OFF] {module_name}")

            print()

        # ==================================
        # REPARAR
        # ==================================

        elif command.lower() == "reparar":

            logger.info("Ejecutando AutoRepair manual...")

            repair.check_dependencies()

            print("Reparación completada.")

        # ==================================
        # MEMORIA FUTURA
        # ==================================

        elif command.lower().startswith("recordar"):

            print(
                "Sistema de memoria aún en desarrollo."
            )

        # ==================================
        # FACE SWAP FUTURO
        # ==================================

        elif "modifica rostro" in command.lower():

            print(
                "Módulo FaceSwap aún en integración."
            )

        # ==================================
        # MEJORA IA FUTURA
        # ==================================

        elif "mejora imagen" in command.lower():

            print(
                "Módulo Enhance AI aún en integración."
            )

        # ==================================
        # COMANDO DESCONOCIDO
        # ==================================

        else:

            print(
                "Comando no reconocido."
            )

    except KeyboardInterrupt:

        logger.warning(
            "Interrupción manual detectada."
        )

        print("\nJarvis detenido.")

        break

    except Exception as error:

        error_manager.handle_error(
            error,
            "MAIN_LOOP"
        )

        print(
            "Ocurrió un error, pero Jarvis sigue estable."
        )

# ==========================================
# INICIAR PANEL
# ==========================================

from ui.main_window import start_ui

start_ui()