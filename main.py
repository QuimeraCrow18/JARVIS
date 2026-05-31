# == AUTOLOADED MODULES START ==
from modules.ai_backends import *
from modules.app_module import *
from modules.automation_module import *
from modules.context_location_proximity_identity_detector_v2 import *
from modules.context_video_vs_real_detector import *
from modules.criminal_behavior_patterns import *
from modules.device_analyzer_module import *
from modules.enhance_module import *
from modules.extortion_analyzer import *
from modules.face_recognition_module import *
from modules.fraud_detection_module import *
from modules.identity_spoofing_detector import *
from modules.interaction_module import *
from modules.knowledge_engine import *
from modules.learning_module import *
from modules.media_module import *
from modules.memory_module import *
from modules.optimizer_module import *
from modules.render_module import *
from modules.secure_communication import *
from modules.swapface_module import *
from modules.swapface_video_gender_blend import *
from modules.system_module import *
from modules.threat_analyzer import *
from modules.voice_module import *
from modules.webremote_module import *
# == AUTOLOADED MODULES END ==

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

face_recognition_module = loader.load_module(
    "modules.face_recognition_module"
)

learning_module = loader.load_module(
    "modules.learning_module"
)

webremote_module = loader.load_module(
    "modules.webremote_module"
)

knowledge_engine_module = loader.load_module(
    "modules.knowledge_engine"
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
    "faces_panel": faces_panel_module,
    "face_recognition": face_recognition_module,
    "learning": learning_module,
    "webremote": webremote_module,
    "knowledge": knowledge_engine_module
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

  Plataforma: {plat}
  Multi-Platform Remote activo
  AutoRepair activo
  SafeLoader activo
  Logs activos
  Modo modular activo
  Auto-Sync GitHub activo

=========================================

""".format(plat=_detector.friendly_name))

# ==========================================
# INICIAR MOTOR DE CONOCIMIENTO
# ==========================================

_knowledge = None
if knowledge_engine_module:
    try:
        _knowledge = knowledge_engine_module.KnowledgeEngine(brain=jarvis_brain)
        logger.info("Motor de conocimiento infinito iniciado.")
        if _knowledge:
            stats = _knowledge.get_stats()
            logger.info(f"Conocimiento: {stats['total_absorbed']} entradas en {stats['topics']} temas")
    except Exception as e:
        logger.warning(f"No se pudo iniciar motor de conocimiento: {e}")

logger.info("Jarvis iniciado correctamente.")

# ==========================================
# DETECTAR PLATAFORMA
# ==========================================

_detector = None
try:
    from plat.detector import PlatformDetector
    _detector = PlatformDetector()
    plat_info = _detector.get_info()
    logger.info(f"Plataforma detectada: {_detector.friendly_name}")
    logger.info(f"Características: {', '.join(_detector.get_available_features())}")
except Exception as e:
    logger.warning(f"No se pudo detectar plataforma: {e}")

# ==========================================
# INICIAR MÓDULO DE APRENDIZAJE
# ==========================================

jarvis_brain = None
if learning_module:
    try:
        jarvis_brain = learning_module.LearningModule()
        logger.info("Módulo de aprendizaje iniciado.")
    except Exception as e:
        logger.warning(f"No se pudo iniciar aprendizaje: {e}")

# ==========================================
# INICIAR UI (INTERFAZ GRÁFICA)
# ==========================================

try:
    from ui.main_window import start_ui as _start_ui
    import threading
    _ui_thread = threading.Thread(target=_start_ui, daemon=True)
    _ui_thread.start()
    logger.info("Interfaz UI iniciada en segundo plano.")
except Exception as e:
    logger.warning(f"No se pudo iniciar la UI: {e}")

# ==========================================
# INICIAR WEB REMOTE (MULTI-PLATAFORMA)
# ==========================================

_web_server = None
if webremote_module and _detector:
    try:
        _web_server = webremote_module.WebRemoteModule(port=8080)
        jarvis_refs = {
            "detector": _detector,
            "brain": jarvis_brain,
            "knowledge": _knowledge,
            "processor": lambda cmd: _process_web_command(cmd, loaded_modules, jarvis_brain)
        }
        _web_server.register_jarvis(**jarvis_refs)
        _web_server.start()
        logger.info(f"Web remote iniciado: {_web_server.get_url()}")
    except Exception as e:
        logger.warning(f"No se pudo iniciar web remote: {e}")


def _process_web_command(cmd, mods, brain):
    cmd_lower = cmd.lower().strip()
    if cmd_lower in ("status",):
        status = []
        for name, data in mods.items():
            status.append(f"[{'OK' if data else 'OFF'}] {name}")
        return "\n".join(status)
    if cmd_lower in ("que sabes", "conocimientos"):
        if brain:
            return f"{brain.get_stats()['facts']} hechos, {brain.get_stats()['conversations']} conversaciones"
        return "Módulo de aprendizaje no disponible"
    if cmd_lower.startswith("recuerda "):
        if brain:
            val = brain.recall_fact(cmd_lower[9:])
            return val or "No lo sé"
        return "No disponible"
    if cmd_lower == "plataforma":
        if _detector:
            info = _detector.get_info()
            return f"{info['friendly_name']} - {info['platform']}"
        return "No detectada"
    return "Comando recibido. Usa el CLI local para más funciones."

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
        # APRENDER
        # ==================================

        elif command.lower().startswith("aprender"):

            if not jarvis_brain:
                print("Módulo de aprendizaje no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                rest = command[len("aprender"):].strip()
                if "=" in rest:
                    key, value = rest.split("=", 1)
                    jarvis_brain.learn_fact(key.strip(), value.strip())
                    jarvis_brain.record_conversation(command,
                        f"Aprendido: {key.strip()} = {value.strip()}")
                else:
                    print("Uso: aprender <clave> = <valor>")

        # ==================================
        # RECORDAR
        # ==================================

        elif command.lower().startswith("recuerda"):

            if not jarvis_brain:
                print("Módulo de aprendizaje no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                if len(parts) >= 2:
                    key = parts[1]
                    value = jarvis_brain.recall_fact(key)
                    if value is not None:
                        print(f"{key}: {value}")
                else:
                    print("Uso: recuerda <clave>")

        # ==================================
        # OLVIDAR
        # ==================================

        elif command.lower().startswith("olvida"):

            if not jarvis_brain:
                print("Módulo de aprendizaje no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                if len(parts) >= 2:
                    jarvis_brain.forget_fact(parts[1])
                else:
                    print("Uso: olvida <clave>")

        # ==================================
        # QUE SABES
        # ==================================

        elif command.lower() in ["que sabes", "qué sabes", "conocimientos", "que sabes?"]:

            if not jarvis_brain:
                print("Módulo de aprendizaje no disponible.")
            else:
                stats = jarvis_brain.get_stats()
                print(f"\nConocimientos: {stats['facts']}")
                print(f"Preferencias: {stats['preferences']}")
                print(f"Conversaciones recordadas: {stats['conversations']}\n")
                jarvis_brain.list_all_facts()

        # ==================================
        # CONVERSACIONES
        # ==================================

        elif command.lower() in ["conversaciones", "historial"]:

            if not jarvis_brain:
                print("Módulo de aprendizaje no disponible.")
            else:
                jarvis_brain.get_recent_conversations()

        # ==================================
        # PLATAFORMA
        # ==================================

        elif command.lower() in ["plataforma", "platform"]:

            if _detector:
                info = _detector.get_info()
                print(f"Plataforma: {info['friendly_name']}")
                print(f"Sistema: {info['system']} ({info['machine']})")
                print(f"Python: {info['python']}")
                print(f"Escritorio: {'Si' if info['is_desktop'] else 'No'}")
                print(f"Pantalla: {'Si' if info['has_display'] else 'No'}")
                feats = _detector.get_available_features()
                print(f"Funciones disponibles: {', '.join(feats)}")
            else:
                print("Detector de plataforma no disponible.")

        # ==================================
        # WEB REMOTE
        # ==================================

        elif command.lower().startswith("web"):

            if not _web_server:
                print("Servidor web no disponible.")
            else:
                parts = command.lower().split()
                if len(parts) >= 2:
                    if parts[1] in ("on", "start", "iniciar"):
                        _web_server.start()
                        print(f"Servidor web iniciado en {_web_server.get_url()}")
                    elif parts[1] in ("off", "stop", "detener"):
                        _web_server.stop()
                        print("Servidor web detenido.")
                    elif parts[1] in ("url", "ip"):
                        print(f"URL: {_web_server.get_url()}")
                    else:
                        print("Uso: web on/off/url")
                else:
                    print(f"Estado: {'activo' if _web_server._running else 'inactivo'}")
                    print(f"URL: {_web_server.get_url()}")

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
        # RECONOCER ROSTRO
        # ==================================

        elif command.lower().startswith("reconocer"):

            if not face_recognition_module:
                print("Módulo de reconocimiento facial no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                if len(parts) >= 2:
                    img = parts[1]
                    result = face_recognition_module.recognize(img)
                    if result:
                        print(f"Rostro reconocido como: {result[0]['name']} "
                              f"({result[0]['confidence']}%)")
                    else:
                        print("No se reconoció ningún rostro conocido.")
                else:
                    print("Uso: reconocer <ruta_imagen>")

        # ==================================
        # REGISTRAR ROSTRO
        # ==================================

        elif command.lower().startswith("registrar rostro"):

            if not face_recognition_module:
                print("Módulo de reconocimiento facial no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                if len(parts) >= 4:
                    img = parts[2]
                    name = parts[3]
                    face_recognition_module.register_face(img, name)
                    print(f"Rostro registrado como: {name}")
                else:
                    print("Uso: registrar rostro <ruta_imagen> <nombre>")

        # ==================================
        # VERIFICAR ROSTROS
        # ==================================

        elif command.lower().startswith("comparar rostros"):

            if not face_recognition_module:
                print("Módulo de reconocimiento facial no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                if len(parts) >= 3:
                    result = face_recognition_module.verify(parts[2], parts[3])
                    if result:
                        if result["verified"]:
                            print(f"Coinciden ({result['confidence']}% confianza)")
                        else:
                            print(f"No coinciden (distancia: {result['distance']})")
                    else:
                        print("Error al comparar.")
                else:
                    print("Uso: comparar rostros <ruta1> <ruta2>")

        # ==================================
        # DETECTAR ROSTROS
        # ==================================

        elif command.lower().startswith("detectar rostros"):

            if not face_recognition_module:
                print("Módulo de reconocimiento facial no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                if len(parts) >= 3:
                    faces = face_recognition_module.detect_faces(parts[2])
                    print(f"{len(faces)} rostro(s) detectado(s).")
                else:
                    print("Uso: detectar rostros <ruta_imagen>")

        # ==================================
        # BUSCAR CONOCIMIENTO
        # ==================================

        elif command.lower().startswith("buscar"):

            if not _knowledge:
                print("Motor de conocimiento no disponible.")
            else:
                query = command[7:].strip()
                if not query:
                    print("Uso: buscar <consulta>")
                else:
                    results = _knowledge.query(query)
                    if results:
                        print(f"\n{len(results)} resultado(s) para: {query}")
                        for i, r in enumerate(results, 1):
                            print(f"\n--- Resultado {i} (fuente: {r['source']}) ---")
                            print(r['content'][:500])
                    else:
                        print(f"No encontré nada sobre \"{query}\" en mi conocimiento.")

        # ==================================
        # ABSORBER CONOCIMIENTO DE URL
        # ==================================

        elif command.lower().startswith("aprende de"):

            if not _knowledge:
                print("Motor de conocimiento no disponible.")
            else:
                import shlex
                parts = shlex.split(command)
                if len(parts) >= 3 and parts[1] == "de":
                    url = parts[2]
                    print(f"Absorbiendo conocimiento de {url}...")
                    ok, msg = _knowledge.absorb_url(url)
                    print(f"Resultado: {msg}")
                else:
                    print("Uso: aprende de <url>")

        # ==================================
        # QUE SABES (MOTOR DE CONOCIMIENTO)
        # ==================================

        elif command.lower() in ["que sabes de conocimiento", "stats conocimiento", "knowledge stats"]:

            if not _knowledge:
                print("Motor de conocimiento no disponible.")
            else:
                stats = _knowledge.get_stats()
                print(f"\n--- Estadísticas de Conocimiento ---")
                print(f"Total absorbido: {stats['total_absorbed']} entradas")
                print(f"Temas: {stats['topics']}")
                print(f"Fuentes: {stats['sources']}")
                print(f"Palabras clave indexadas: {stats['keywords_indexed']}")
                print(f"En esta sesion: {stats['session_absorbed']}")
                topics = _knowledge.get_topics()
                if topics:
                    print(f"\nTemas disponibles: {', '.join(topics[:20])}")

        # ==================================
        # TEMAS DE CONOCIMIENTO
        # ==================================

        elif command.lower().startswith("temas"):

            if not _knowledge:
                print("Motor de conocimiento no disponible.")
            else:
                topics = _knowledge.get_topics()
                if topics:
                    print(f"\nTemas ({len(topics)}):")
                    for t in sorted(topics):
                        print(f"  - {t}")
                else:
                    print("No hay temas registrados aun.")

        # ==================================
        # OLVIDAR TEMA
        # ==================================

        elif command.lower().startswith("olvida tema"):

            if not _knowledge:
                print("Motor de conocimiento no disponible.")
            else:
                topic = command[12:].strip()
                if topic:
                    ok, msg = _knowledge.forget_topic(topic)
                    print(msg)
                else:
                    print("Uso: olvida tema <nombre_tema>")

        # ==================================
        # IA - PREGUNTAR A BACKENDS
        # ==================================

        elif command.lower().startswith("ia"):

            if not _knowledge:
                print("Motor de conocimiento no disponible.")
            else:
                query = command[3:].strip()
                if not query:
                    backends = _knowledge.get_available_ai_backends()
                    if backends:
                        print(f"Backends IA disponibles: {', '.join(backends.keys())}")
                    else:
                        print("No hay backends IA disponibles. Usa: 'ia <pregunta>'")
                else:
                    print(f"Consultando a las IAs sobre: {query}")
                    ok, msg = _knowledge.absorb_from_ai(query)
                    result = _knowledge.query(query, max_results=1)
                    if result:
                        print(f"\n{result[0]['content'][:600]}")
                    else:
                        print(f"No se pudo obtener respuesta. {msg}")

        # ==================================
        # LISTAR BACKENDS IA
        # ==================================

        elif command.lower() in ["ia backends", "backends"]:

            if not _knowledge:
                print("Motor de conocimiento no disponible.")
            else:
                all_b = _knowledge.get_all_ai_backends()
                avail = _knowledge.get_available_ai_backends()
                print("\n--- Backends IA ---")
                for name, backend in all_b.items():
                    status = "DISPONIBLE" if name in avail else "NO DISP."
                    print(f"  {name}: {status}")
                if not all_b:
                    print("  (no se encontraron backends)")

        # ==================================
        # COMANDO DESCONOCIDO
        # ==================================

        else:

            msg = "Comando no reconocido."
            print(msg)
            if jarvis_brain:
                jarvis_brain.record_conversation(command, msg)

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

