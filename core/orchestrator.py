import json
import os
import sys
import threading
from datetime import datetime

from core.auto_repair import AutoRepair
from core.safe_loader import SafeLoader
from core.logger import JarvisLogger
from core.error_manager import ErrorManager
from modules.event_bus import EventBus, publish_event, request_response
from modules.cognition_router import CognitionRouter
from modules.sentinel import Sentinel
from core.hardware_awareness import HardwareDetector
from modules.mesh_gateway import MeshGateway
from modules.vpn_bridge import VPNSecureTunnel, get_bridge


class Orchestrator:
    def __init__(self):
        self.logger = None
        self.error_manager = None
        self.repair = None
        self.loader = None

        # Safe-loaded modules
        self.voice_module = None
        self.media_module = None
        self.enhance_module = None
        self.automation_module = None
        self.memory_module = None
        self.render_module = None
        self.faces_panel_module = None
        self.face_recognition_module = None
        self.learning_module = None
        self.webremote_module = None
        self.knowledge_engine_module = None
        self.code_analyzer_module = None

        # Direct-import modules
        self.system_module = None
        self.system_controller = None
        self.swapface_module = None
        self.search_module = None

        self.loaded_modules = {}
        self._detector = None
        self.jarvis_brain = None
        self._knowledge = None
        self._code_analyzer = None
        self._voice_listener = None
        self._mic_control = None
        self._web_server = None
        self.dispatcher = None
        self.event_bus = None
        self._hardware = None
        self.router = None
        self.sentinel = None
        self._vpn = None
        self._mesh = None

    # ==========================================
    # SETUP
    # ==========================================

    def setup(self):
        self._init_logger()
        self._init_hardware()
        self._init_event_bus()
        self._init_cognition_router()
        self._init_error_manager()
        self._init_repair()
        self._init_loader()
        self._load_config()
        self._safe_imports()
        self._init_modules()
        self._register_modules()
        self._init_platform()
        self._init_brain()
        self._init_knowledge()
        self._init_code_analyzer()
        self._boot_screen()
        self._init_dispatcher()
        self._init_background_thought()
        self._init_voice()
        self._init_handshake()
        self._init_shield()
        self._init_sentinel()
        self._init_mesh()
        self._init_vpn()
        self._init_auto_patcher()
        self._init_pre_flight()
        self._init_voice_engine()
        self._init_media_processor()

    def _init_logger(self):
        self.logger = JarvisLogger()
        self.logger.info("=================================")
        self.logger.info("INICIANDO JARVIS")
        self.logger.info("=================================")

    def _init_hardware(self):
        self._hardware = HardwareDetector()
        report = self._hardware.run()
        self.logger.info(f"[SYSTEM] Hardware detectado: {report['profile'].upper()} ({report['system']})")
        self._boot_flags = self._hardware.get_boot_flags()
        self.logger.info(f"[SYSTEM] Boot flags: {self._boot_flags}")

    def _init_event_bus(self):
        self.event_bus = EventBus()
        self.logger.info("[SYSTEM] Fase 5: Event Bus activado y listo.")

    def _init_cognition_router(self):
        self.router = CognitionRouter()
        def _route_handler(request):
            payload = request.get("payload", {})
            result = self.router.route(
                prompt=payload.get("prompt", ""),
                tier=payload.get("tier", "balanced"),
            )
            return {"status": "success" if result.get("success") else "error", **result}
        self.event_bus.register_handler("cognition.route", _route_handler)
        self.logger.info("[SYSTEM] Cognition Router conectado al Event Bus.")

    def _init_error_manager(self):
        self.error_manager = ErrorManager()

    def _init_repair(self):
        self.logger.info("Iniciando sistema AutoRepair...")
        self.repair = AutoRepair()
        self.repair.check_dependencies()
        self.logger.info("AutoRepair finalizado.")

    def _init_loader(self):
        self.logger.info("Cargando modulos seguros...")
        self.loader = SafeLoader()

    def _load_config(self):
        self._enabled_modules = {}
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json")
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
            self._enabled_modules = cfg.get("modules", {})
        except Exception as e:
            self.logger.warning(f"No se pudo cargar config: {e}")

    def _should_load(self, name):
        return self._enabled_modules.get(name, True)

    def _safe_imports(self):
        if self._should_load("voice"):
            self.voice_module = self.loader.load_module("voice")
        if self._should_load("media"):
            self.media_module = self.loader.load_module("modules.media_module")
        if self._should_load("enhance"):
            self.enhance_module = self.loader.load_module("modules.enhance_module")
        if self._should_load("automation"):
            self.automation_module = self.loader.load_module("modules.automation_module")
        if self._should_load("memory"):
            self.memory_module = self.loader.load_module("modules.memory_module")
        if self._should_load("render"):
            self.render_module = self.loader.load_module("ui.render_panel")
        if self._should_load("faces_panel"):
            self.faces_panel_module = self.loader.load_module("ui.faces_panel")
        if self._should_load("face_recognition"):
            self.face_recognition_module = self.loader.load_module("modules.face_recognition_module")
        if self._should_load("learning"):
            self.learning_module = self.loader.load_module("modules.learning_module")
        if self._should_load("webremote"):
            self.webremote_module = self.loader.load_module("modules.webremote_module")
        if self._should_load("knowledge"):
            self.knowledge_engine_module = self.loader.load_module("modules.knowledge_engine")
        if self._should_load("code_analyzer"):
            self.code_analyzer_module = self.loader.load_module("modules.code_analyzer")

    def _init_modules(self):
        self.system_module = None
        if self._should_load("system"):
            try:
                from modules.system_module import SystemModule
                self.system_module = SystemModule()
                self.logger.info("[OK] system")
            except Exception as e:
                self.logger.warning(f"[DESACTIVADO] system: {e}")

        self.system_controller = None
        if self._should_load("system_controller"):
            try:
                from modules.system_controller import SystemController
                self.system_controller = SystemController()
                self.logger.info("[OK] system_controller")
            except Exception as e:
                self.logger.warning(f"[DESACTIVADO] system_controller: {e}")

        self.swapface_module = None
        if self._should_load("swapface"):
            try:
                from modules.swapface_module import SwapFaceModule
                self.swapface_module = SwapFaceModule()
                self.logger.info("[OK] swapface")
            except Exception as e:
                self.logger.warning(f"[DESACTIVADO] swapface: {e}")

        self.search_module = None
        if self._should_load("search"):
            try:
                from modules.search_module import SearchModule
                self.search_module = SearchModule()
                self.logger.info("[OK] search")
            except Exception as e:
                self.logger.warning(f"[DESACTIVADO] search: {e}")

    def _register_modules(self):
        self.loaded_modules = {
            "voice": self.voice_module,
            "media": self.media_module,
            "enhance": self.enhance_module,
            "automation": self.automation_module,
            "memory": self.memory_module,
            "render": self.render_module,
            "faces_panel": self.faces_panel_module,
            "face_recognition": self.face_recognition_module,
            "learning": self.learning_module,
            "webremote": self.webremote_module,
            "knowledge": self.knowledge_engine_module,
            "code_analyzer": self.code_analyzer_module,
            "system": self.system_module,
            "system_controller": self.system_controller,
            "swapface": self.swapface_module,
            "search": self.search_module,
        }

        try:
            from modules._registry import AUTO_MODULES
            explicit = set(self.loaded_modules.keys())
            for name in AUTO_MODULES:
                safe = name.replace("_module", "").replace("_", "")
                if safe not in explicit and name not in explicit:
                    if not self._should_load(safe):
                        continue
                    mod = self.loader.load_module(f"modules.{name}")
                    if mod:
                        self.loaded_modules[name] = mod
        except Exception:
            pass

        for name, data in self.loaded_modules.items():
            if data:
                self.logger.info(f"[OK] {name}")
            else:
                self.logger.warning(f"[DESACTIVADO] {name}")

    def _init_platform(self):
        self._detector = None
        try:
            from plat.detector import PlatformDetector
            self._detector = PlatformDetector()
            info = self._detector.get_info()
            self.logger.info(f"Plataforma detectada: {self._detector.friendly_name}")
            self.logger.info(f"Caracteristicas: {', '.join(self._detector.get_available_features())}")
        except Exception as e:
            self.logger.warning(f"No se pudo detectar plataforma: {e}")

    def _init_brain(self):
        self.jarvis_brain = None
        if self.learning_module:
            try:
                self.jarvis_brain = self.learning_module.LearningModule()
                self.logger.info("Modulo de aprendizaje iniciado.")
            except Exception as e:
                self.logger.warning(f"No se pudo iniciar aprendizaje: {e}")

    def _init_knowledge(self):
        self._knowledge = None
        if self.knowledge_engine_module:
            try:
                self._knowledge = self.knowledge_engine_module.KnowledgeEngine(brain=self.jarvis_brain)
                self.logger.info("Motor de conocimiento infinito iniciado.")
                if self._knowledge:
                    stats = self._knowledge.get_stats()
                    self.logger.info(f"Conocimiento: {stats['total_absorbed']} entradas en {stats['topics']} temas")
            except Exception as e:
                self.logger.warning(f"No se pudo iniciar motor de conocimiento: {e}")

    def _init_code_analyzer(self):
        self._code_analyzer = None
        if self.code_analyzer_module:
            try:
                self._code_analyzer = self.code_analyzer_module.CodeAnalyzer(
                    knowledge_engine=self._knowledge,
                    ai_manager=self._knowledge._ai_manager if self._knowledge else None
                )
                self.logger.info("Analizador de codigo multilenguaje iniciado.")
            except Exception as e:
                self.logger.warning(f"No se pudo iniciar analizador de codigo: {e}")

    def _boot_screen(self):
        plat = self._detector.friendly_name if self._detector else "Desconocida"
        handshake_mode = self._handshake.mode if self._handshake else "N/A"
        shield_status = "ON" if self._shield else "OFF"
        sentinel_status = "ON" if self._sentinel else "OFF"
        vpn_status = "ON" if self._vpn else "OFF"
        mesh_status = "ON" if self._mesh else "OFF"
        voice_engine = "edge-tts" if self._voice_engine else "pyttsx3"
        print(f"""
=========================================
            JARVIS ONLINE v2.0
=========================================

  Plataforma: {plat}
  Multi-Platform Remote activo
  AutoRepair activo
  SafeLoader activo
  Logs activos
  Modo modular activo
  Auto-Sync GitHub activo
  Handshake: {handshake_mode}
  Shield Anti-Spam: {shield_status}
  Sentinel Heartbeat: {sentinel_status}
  Voice Engine: {voice_engine}
  VPN Bridge: {vpn_status}
  Mesh Cluster: {mesh_status}

========================================
""")
        self.logger.info("Jarvis v2.0 iniciado correctamente.")

    def _init_dispatcher(self):
        self.dispatcher = None
        try:
            from core.dispatcher import Dispatcher
            self.dispatcher = Dispatcher(
                controller=self.system_controller,
                voice_module=self._voice_listener,
            )
            self.logger.info("[OK] dispatcher")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] dispatcher: {e}")

    def _get_api_key(self):
        try:
            import json
            import os
            cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json")
            with open(cfg_path) as f:
                cfg = json.load(f)
            return cfg.get("brain", {}).get("api_key", "")
        except Exception:
            return ""

    def _init_background_thought(self):
        try:
            from core.brain import background_thought
            api_key = self._get_api_key()
            background_thought.start_background_evolution(api_key)
            self.logger.info("[OK] background_thought")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] background_thought: {e}")

    def _init_voice(self):
        self._voice_listener = None
        self._mic_control = None
        try:
            from modules.voice_module import VoiceModule
            self._voice_listener = VoiceModule()

            # Usar Dispatcher como puente voz → sistema
            if self.dispatcher:
                self.dispatcher.set_voice(self._voice_listener)
                self._voice_listener.set_command_callback(self.dispatcher.make_voice_callback())
            else:
                def _voice_callback(cmd):
                    print(f"[VOICE] Procesando comando: {cmd}")
                    sm = self.system_module
                    if sm and ("sistema" in cmd or "recursos" in cmd):
                        s = sm.get_stats()
                        self._voice_listener.speak(f"CPU al {s['cpu']}%, RAM al {s['ram']['percent']}%")
                    elif sm and "apagar" in cmd:
                        sm.shutdown()
                    elif sm and "reiniciar" in cmd:
                        sm.restart()
                    elif "status" in cmd or "estado" in cmd:
                        self._voice_listener.speak("Todos los modulos operativos")
                    elif "hora" in cmd:
                        self._voice_listener.speak(f"Son las {datetime.now().strftime('%H:%M')}")
                    else:
                        self._voice_listener.speak("Comando no reconocido")

                self._voice_listener.set_command_callback(_voice_callback)

            from modules.microphone_control import MicrophoneControl, _set_instance
            self._mic_control = MicrophoneControl(voice_listener=self._voice_listener, brain=self.jarvis_brain)
            _set_instance(self._mic_control)

            if self._mic_control.get_microphone_status():
                self._voice_listener.start_listening()
                self.logger.info("Escucha por voz iniciada (wake word: 'jarvis')")
            else:
                self.logger.info("Microfono silenciado segun configuracion guardada")
        except Exception as e:
            self.logger.warning(f"No se pudo iniciar escucha por voz: {e}")

    # ==========================================
    # FASE 1-5: NEW MODULES
    # ==========================================

    def _init_handshake(self):
        self._handshake = None
        try:
            from modules.handshake import HandshakeProtocol
            self._handshake = HandshakeProtocol()
            self._handshake.check_connection()
            self._handshake.start_background_sync()
            mode = self._handshake.mode
            self.logger.info(f"[OK] handshake (modo: {mode})")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] handshake: {e}")

    def _init_shield(self):
        self._shield = None
        try:
            from modules.shield_module import ShieldModule
            self._shield = ShieldModule()
            self.logger.info("[OK] shield_module")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] shield_module: {e}")

    def _init_sentinel(self):
        self._sentinel = None
        self.sentinel = None
        try:
            from modules.sentinel import Sentinel
            self._sentinel = Sentinel()
            self.sentinel = self._sentinel
            for name, mod in self.loaded_modules.items():
                if mod is not None:
                    self._sentinel.register_module(name, mod)
            self._sentinel.start()
            self.event_bus.subscribe("cognition.model.failure", lambda e: self._sentinel._check_all())
            self.logger.info("[OK] sentinel")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] sentinel: {e}")

    def _init_mesh(self):
        self._mesh = None
        try:
            self._mesh = MeshGateway()
            self.event_bus.register_handler("cluster.negotiate", lambda r: self._mesh._handle_cluster_negotiate(r))
            self.event_bus.register_handler("cluster.distribute", lambda r: self._mesh._handle_distribute(r))
            self.event_bus.register_handler("cluster.should_delegate", lambda r: self._mesh._handle_should_delegate(r))
            self.logger.info("[OK] mesh_gateway (cluster activo)")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] mesh_gateway: {e}")

    def _init_vpn(self):
        self._vpn = None
        try:
            self._vpn = VPNSecureTunnel()
            self.event_bus.register_handler("vpn.handshake", lambda r: self._vpn._handle_handshake(r))
            self.event_bus.register_handler("vpn.send", lambda r: self._vpn._handle_send(r))
            self.event_bus.register_handler("vpn.task", lambda r: self._vpn._handle_task(r))
            self._vpn.event_bus = self.event_bus
            self.event_bus.subscribe("vpn.task_completed", lambda e: self.logger.info(f"[VPN] Tarea completada: {e.get('result','?')}"))
            self._start_cpu_delegator()
            self.logger.info("[OK] vpn_bridge (tunel cifrado activo)")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] vpn_bridge: {e}")

    def _start_cpu_delegator(self):
        def _monitor():
            import time
            import psutil
            while True:
                try:
                    cpu = psutil.cpu_percent(interval=2.0)
                    if cpu > 80 and self._mesh and self._vpn:
                        self.logger.info(f"[DELEGATOR] CPU al {cpu}% — evaluando delegacion...")
                        targets = [n for n in self._mesh.nodes if n.get("alive")]
                        if targets:
                            target = targets[0]["name"]
                            self.logger.info(f"[DELEGATOR] Tarea ligera delegada a {target}")
                            publish_event("vpn.send", {
                                "target": target,
                                "task_type": "maintenance",
                                "data": {"cpu": cpu, "reason": "high_load"}
                            }, "orchestrator")
                except Exception:
                    pass
                time.sleep(30)
        t = threading.Thread(target=_monitor, daemon=True)
        t.start()
        self.logger.info("[DELEGATOR] Monitor de carga CPU iniciado (check cada 30s)")

    def _init_auto_patcher(self):
        self._auto_patcher = None
        try:
            from modules.auto_patcher import AutoPatcher
            self._auto_patcher = AutoPatcher()
            self.logger.info("[OK] auto_patcher")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] auto_patcher: {e}")

    def _init_pre_flight(self):
        self._pre_flight = None
        try:
            from modules.pre_flight import PreFlight
            self._pre_flight = PreFlight()
            result = self._pre_flight.run_all()
            self.logger.info(f"[OK] pre_flight ({result['passed']}/{result['total']})")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] pre_flight: {e}")

    def _init_voice_engine(self):
        self._voice_engine = None
        try:
            from modules.voice_engine import VoiceEngine
            self._voice_engine = VoiceEngine()
            self.logger.info("[OK] voice_engine (edge-tts)")

            # --- PARCHE DE CONEXIÓN DE VOZ ---
            if hasattr(self, '_voice_listener') and self._voice_listener:
                try:
                    self._voice_engine.set_voice_listener(self._voice_listener)
                    self._voice_engine.set_brain(self.jarvis_brain)
                    self._voice_engine.enable_microphone()
                    self.logger.info("[SYSTEM] Conexion de voz establecida: Listener y Brain enlazados.")
                except AttributeError as e:
                    self.logger.warning(f"[ERROR] Fallo al enlazar modulos de voz: {e}")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] voice_engine: {e}")

    def _init_media_processor(self):
        self._media_processor = None
        try:
            from modules.media_processor import MediaProcessor
            self._media_processor = MediaProcessor()
            self.logger.info("[OK] media_processor")
        except Exception as e:
            self.logger.warning(f"[DESACTIVADO] media_processor: {e}")

    # ==========================================
    # UI / WEB
    # ==========================================

    def get_web_refs(self):
        refs = {
            "detector": self._detector,
            "brain": self.jarvis_brain,
            "knowledge": self._knowledge,
            "code_analyzer": self._code_analyzer,
            "processor": self.process_command,
        }
        if self._mic_control:
            refs["mic_control"] = self._mic_control
        if self._voice_listener:
            refs["voice"] = self._voice_listener
        if self.system_module:
            refs["system"] = self.system_module
        if self.swapface_module:
            refs["swapface"] = self.swapface_module
        if self.search_module:
            refs["search"] = self.search_module
        if self.system_controller:
            refs["system_controller"] = self.system_controller
        if self.dispatcher:
            refs["dispatcher"] = self.dispatcher
        return refs

    def get_ui_refs(self):
        try:
            from core.command_router import execute_command as router_fn
        except Exception:
            router_fn = None
        try:
            import core.file_manager as file_mgr
        except Exception:
            file_mgr = None
        refs = {
            "system": self.system_module,
            "search": self.search_module,
            "swapface": self.swapface_module,
            "brain": self.jarvis_brain,
            "knowledge": self._knowledge,
            "code_analyzer": self._code_analyzer,
            "detector": self._detector,
            "web": lambda: self._web_server,
            "repair": self.repair,
            "face_recognition": self.face_recognition_module,
            "mic_control": self._mic_control,
            "file_manager": file_mgr,
            "router": router_fn,
        }
        if self._shield:
            refs["shield"] = self._shield
        if self._sentinel:
            refs["sentinel"] = self._sentinel
        if self._voice_engine:
            refs["voice_engine"] = self._voice_engine
        if self._media_processor:
            refs["media_processor"] = self._media_processor
        if self._handshake:
            refs["handshake"] = self._handshake
        return refs

    def start_ui(self):
        try:
            from ui.main_window import start_ui
            thread = threading.Thread(target=start_ui, kwargs={"jarvis_refs": self.get_ui_refs()}, daemon=True)
            thread.start()
            self.logger.info("Interfaz UI iniciada en segundo plano.")
        except Exception as e:
            self.logger.warning(f"No se pudo iniciar la UI: {e}")

    def start_web(self, port=8080):
        self._web_server = None
        if self.webremote_module and self._detector:
            try:
                self._web_server = self.webremote_module.WebRemoteModule(port=port)
                self._web_server.register_jarvis(**self.get_web_refs())
                self._web_server.start()
                self.logger.info(f"Web remote iniciado: {self._web_server.get_url()}")
            except Exception as e:
                self.logger.warning(f"No se pudo iniciar web remote: {e}")

    # ==========================================
    # UNIFIED COMMAND PROCESSOR
    # ==========================================

    def process_command(self, cmd):
        cmd_lower = cmd.lower().strip()

        if cmd_lower == "status":
            lines = []
            for name, data in self.loaded_modules.items():
                lines.append(f"[{'OK' if data else 'OFF'}] {name}")
            return "\n".join(lines)

        if cmd_lower == "reparar":
            self.repair.check_dependencies()
            return "Reparacion completada."

        if cmd_lower.startswith("aprender "):
            if not self.jarvis_brain:
                return "Modulo de aprendizaje no disponible"
            rest = cmd[len("aprender"):].strip()
            if "=" in rest:
                key, value = rest.split("=", 1)
                self.jarvis_brain.learn_fact(key.strip(), value.strip())
                self.jarvis_brain.record_conversation(cmd, f"Aprendido: {key.strip()} = {value.strip()}")
                return f"Aprendido: {key.strip()} = {value.strip()}"
            return "Uso: aprender <clave> = <valor>"

        if cmd_lower.startswith("recuerda "):
            if not self.jarvis_brain:
                return "No disponible"
            val = self.jarvis_brain.recall_fact(cmd_lower[9:])
            return val or "No lo se"

        if cmd_lower.startswith("olvida "):
            if not self.jarvis_brain:
                return "No disponible"
            self.jarvis_brain.forget_fact(cmd_lower[7:].strip())
            return "Olvidado."

        if cmd_lower in ("que sabes", "que sabes?", "conocimientos"):
            if not self.jarvis_brain:
                return "Modulo de aprendizaje no disponible"
            stats = self.jarvis_brain.get_stats()
            lines = [
                f"Conocimientos: {stats['facts']}",
                f"Preferencias: {stats['preferences']}",
                f"Conversaciones: {stats['conversations']}",
            ]
            facts = self.jarvis_brain.list_all_facts()
            if facts:
                lines.append("")
                for k, v in facts.items():
                    lines.append(f"  {k}: {v}")
            return "\n".join(lines)

        if cmd_lower in ("conversaciones", "historial"):
            if not self.jarvis_brain:
                return "No disponible"
            convos = self.jarvis_brain.get_recent_conversations()
            if isinstance(convos, list):
                return "\n".join([f"{c.get('user','?')}: {c.get('jarvis','?')}" for c in convos[-10:]])
            return str(convos)

        if cmd_lower in ("plataforma", "platform"):
            if not self._detector:
                return "No detectada"
            info = self._detector.get_info()
            feats = self._detector.get_available_features()
            return (f"Plataforma: {info['friendly_name']}\nSistema: {info['system']}\n"
                    f"Python: {info['python']}\nFunciones: {', '.join(feats)}")

        if cmd_lower.startswith("web "):
            if not self._web_server:
                return "Servidor web no disponible"
            parts = cmd_lower.split()
            if len(parts) >= 2:
                if parts[1] in ("on", "start", "iniciar"):
                    self._web_server.start()
                    return f"Servidor web iniciado en {self._web_server.get_url()}"
                elif parts[1] in ("off", "stop", "detener"):
                    self._web_server.stop()
                    return "Servidor web detenido."
                elif parts[1] in ("url", "ip"):
                    return f"URL: {self._web_server.get_url()}"
            return f"Estado: {'activo' if self._web_server._running else 'inactivo'} | URL: {self._web_server.get_url()}"

        if cmd_lower in ("sistema", "recursos", "system stats"):
            if not self.system_module:
                return "System module no disponible"
            s = self.system_module.get_stats()
            lines = [f"CPU: {s['cpu']}%"]
            if s.get('cpu_freq'):
                lines.append(f"Frecuencia: {s['cpu_freq']['current']} MHz")
            lines.append(f"RAM: {s['ram']['percent']}% ({s['ram']['used_gb']}/{s['ram']['total_gb']} GB)")
            lines.append(f"Swap: {s['swap']['percent']}%")
            for d in s.get('disk', []):
                lines.append(f"Disco {d['mount']}: {d['percent']}% ({d['used_gb']}/{d['total_gb']} GB)")
            lines.append(f"Red: ↓{s['network']['recv_speed']} MB/s  ↑{s['network']['sent_speed']} MB/s")
            up = int(s['uptime'])
            lines.append(f"Activo: {up//86400}d {(up%86400)//3600}h {(up%3600)//60}m")
            if s.get('battery'):
                bat = s['battery']
                lines.append(f"Bateria: {bat['percent']}% {'(enchufado)' if bat.get('plugged') else '(desenchufado)'}")
            return "\n".join(lines)

        if cmd_lower.startswith("swapface "):
            if not self.swapface_module:
                return "SwapFace module no disponible"
            parts = cmd.split()
            if len(parts) >= 4 and parts[1].lower() == "swap":
                out = parts[4] if len(parts) >= 5 else None
                result = self.swapface_module.swap_faces(parts[2], parts[3], out)
                if result:
                    return f"Rostros intercambiados. Resultado: {result}"
                return "Error al intercambiar rostros."
            return "Uso: swapface swap <img1> <img2> [output]"

        if cmd_lower.startswith("busca archivo "):
            q = cmd_lower[14:].strip()
            if self.search_module and q:
                res = self.search_module.find_files(os.path.expanduser("~"), query=q, max_results=10)
                if res:
                    return "\n".join([f"{r['path']} ({r['size_kb']} KB)" for r in res])
                return "No se encontraron archivos."
            return "Uso: busca archivo <nombre>"

        if cmd_lower.startswith("busca imagen "):
            q = cmd_lower[13:].strip()
            if self.search_module:
                path = q or os.path.expanduser("~")
                res = self.search_module.find_images(path, max_results=10)
                if res:
                    return "\n".join([f"{r['name']} ({r['width']}x{r['height']}, {r['size_kb']} KB)" for r in res])
                return "No se encontraron imagenes."
            return "Search module no disponible"

        if cmd_lower.startswith("duplicados"):
            path = cmd_lower[11:].strip() or os.path.expanduser("~")
            if not self.search_module:
                return "Search module no disponible"
            res = self.search_module.find_duplicates(path)
            if res:
                return "\n".join([f"Original: {r['original']}\nDuplicado: {r['duplicate']}" for r in res[:10]])
            return "No se encontraron duplicados."

        if cmd_lower.startswith("voz "):
            if not self._voice_listener:
                return "Voice module no disponible"
            parts = cmd_lower.split()
            if len(parts) >= 2:
                if parts[1] in ("on", "iniciar", "start"):
                    self._voice_listener.start_listening()
                    return "Escucha por voz iniciada."
                elif parts[1] in ("off", "detener", "stop"):
                    self._voice_listener.stop_listening()
                    return "Escucha por voz detenida."
                elif parts[1] in ("test", "prueba"):
                    self._voice_listener.speak("Hola, soy Jarvis. Todo funciona correctamente.")
                    return "Prueba de voz: JARVIS funcionando correctamente."
                elif parts[1] == "escucha":
                    text = self._voice_listener.listen_once()
                    return f"Reconocido: {text}" if text else "No se detecto voz."
            return "Uso: voz on/off/test/escucha"

        if cmd_lower in ("silenciar", "mute", "mute mic", "desactivar microfono"):
            if self._mic_control:
                return self._mic_control.disable_microphone()
            return "Control de microfono no disponible"
        if cmd_lower in ("activar microfono", "unmute", "unmute mic"):
            if self._mic_control:
                return self._mic_control.enable_microphone()
            return "Control de microfono no disponible"
        if cmd_lower in ("microfono", "toggle mic", "mic"):
            if self._mic_control:
                return self._mic_control.toggle_microphone()
            return "Control de microfono no disponible"

        if cmd_lower.startswith("reconocer ") and self.face_recognition_module:
            img_path = cmd_lower[10:].strip()
            if img_path:
                result = self.face_recognition_module.recognize(img_path)
                if result:
                    return f"Rostro: {result[0]['name']} ({result[0]['confidence']}%)"
                return "No se reconocio ningun rostro conocido."
            return "Uso: reconocer <ruta_imagen>"

        if cmd_lower.startswith("registrar rostro ") and self.face_recognition_module:
            parts = cmd.split()
            if len(parts) >= 4:
                self.face_recognition_module.register_face(parts[2], parts[3])
                return f"Rostro registrado como: {parts[3]}"
            return "Uso: registrar rostro <ruta> <nombre>"

        if cmd_lower.startswith("comparar rostros ") and self.face_recognition_module:
            parts = cmd.split()
            if len(parts) >= 3:
                result = self.face_recognition_module.verify(parts[2], parts[3])
                if result:
                    if result.get("verified"):
                        return f"Coinciden ({result['confidence']}% confianza)"
                    return f"No coinciden (distancia: {result.get('distance','?')})"
                return "Error al comparar."
            return "Uso: comparar rostros <ruta1> <ruta2>"

        if cmd_lower.startswith("detectar rostros ") and self.face_recognition_module:
            parts = cmd.split()
            if len(parts) >= 3:
                faces = self.face_recognition_module.detect_faces(parts[2])
                return f"{len(faces)} rostro(s) detectado(s)."
            return "Uso: detectar rostros <ruta_imagen>"

        if cmd_lower.startswith("buscar ") and self._knowledge:
            query = cmd_lower[7:].strip()
            if query:
                results = self._knowledge.query(query)
                if results:
                    lines = [f"{len(results)} resultado(s) para: {query}"]
                    for i, r in enumerate(results, 1):
                        lines.append(f"\n--- Resultado {i} ({r.get('source','?')}) ---")
                        lines.append(r.get('content','')[:500])
                    return "\n".join(lines)
                return f"No encontre nada sobre '{query}'."
            return "Uso: buscar <consulta>"

        if cmd_lower.startswith("aprende de ") and self._knowledge:
            url = cmd_lower[11:].strip()
            if url:
                ok, msg = self._knowledge.absorb_url(url)
                return f"Resultado: {msg}"
            return "Uso: aprende de <url>"

        if cmd_lower in ("temas",):
            if not self._knowledge:
                return "Motor de conocimiento no disponible"
            topics = self._knowledge.get_topics()
            if topics:
                return f"Temas ({len(topics)}):\n" + "\n".join([f"  - {t}" for t in sorted(topics)])
            return "No hay temas registrados aun."

        if cmd_lower.startswith("olvida tema ") and self._knowledge:
            topic = cmd_lower[12:].strip()
            if topic:
                ok, msg = self._knowledge.forget_topic(topic)
                return msg
            return "Uso: olvida tema <nombre_tema>"

        if cmd_lower.startswith("ia "):
            if not self._knowledge:
                return "Motor de conocimiento no disponible"
            query = cmd_lower[3:].strip()
            if not query:
                backends = self._knowledge.get_available_ai_backends()
                if backends:
                    return f"Backends IA: {', '.join(backends.keys())}"
                return "No hay backends IA disponibles."
            ok, msg = self._knowledge.absorb_from_ai(query)
            results = self._knowledge.query(query, max_results=1)
            if results:
                return results[0].get('content', '')[:600]
            return f"No se pudo obtener respuesta. {msg}"

        if cmd_lower in ("ia backends", "backends"):
            if not self._knowledge:
                return "Motor de conocimiento no disponible"
            all_b = self._knowledge.get_all_ai_backends()
            avail = self._knowledge.get_available_ai_backends()
            lines = ["--- Backends IA ---"]
            for name in all_b:
                status = "DISPONIBLE" if name in avail else "NO DISP."
                lines.append(f"  {name}: {status}")
            return "\n".join(lines) if len(lines) > 1 else "No se encontraron backends."

        if cmd_lower.startswith("analiza ") and self._code_analyzer:
            codigo = cmd.split(None, 1)
            if len(codigo) >= 2:
                res = self._code_analyzer.analizar(codigo[1])
                if res.get("error"):
                    return f"Error: {res['error']}"
                lines = [
                    f"Lenguaje: {res.get('lenguaje','?')}",
                    f"Lineas: {res.get('lineas',0)}",
                    f"Funciones: {res.get('total_funciones',0)}",
                    f"Clases: {res.get('total_clases',0)}",
                ]
                for fn in res.get('funciones', [])[:10]:
                    lines.append(f"  fn: {fn.get('nombre','?')}")
                for cls in res.get('clases', [])[:10]:
                    lines.append(f"  class: {cls.get('nombre','?')}")
                return "\n".join(lines)
            return "Uso: analiza <codigo>"

        if cmd_lower.startswith("explica ") and self._code_analyzer:
            codigo = cmd.split(None, 1)
            if len(codigo) >= 2:
                res = self._code_analyzer.explicar(codigo[1])
                return res.get('explicacion', 'Sin explicacion')[:800]
            return "Uso: explica <codigo>"

        if cmd_lower.startswith("traduce ") and self._code_analyzer:
            parts = cmd.split(None, 2)
            if len(parts) >= 3:
                destino = parts[1].lower()
                codigo = parts[2]
                origen = self._code_analyzer.detectar_lenguaje(codigo)
                res = self._code_analyzer.traducir(codigo, origen=origen, destino=destino)
                if res.get("ok"):
                    return f"--- Codigo {destino.upper()} ---\n{res['codigo']}"
                return "No se pudo traducir."
            return "Uso: traduce <destino> <codigo>"

        if cmd_lower.startswith("que lenguaje es ") and self._code_analyzer:
            codigo = cmd.split(None, 3)
            if len(codigo) >= 2:
                lang = self._code_analyzer.detectar_lenguaje(codigo[-1])
                return f"Lenguaje detectado: {lang}"
            return "Uso: que lenguaje es <codigo>"

        if cmd_lower.startswith("genera codigo ") and self._code_analyzer:
            lenguaje = cmd_lower[14:].strip()
            if lenguaje:
                return f"Para generar codigo {lenguaje}, usa el CLI local (requiere entrada interactiva)."
            return "Uso: genera codigo <lenguaje>"

        if cmd_lower.startswith("indexa codigo ") and self._code_analyzer and self._knowledge:
            codigo = cmd.split(None, 2)
            if len(codigo) >= 2:
                ok, msg = self._code_analyzer.indexar_en_conocimiento(codigo[1])
                return msg
            return "Uso: indexa codigo <codigo>"

        if "modifica rostro" in cmd_lower:
            return "Modulo FaceSwap disponible via web o comando 'swapface swap'."
        if "mejora imagen" in cmd_lower:
            return "Modulo Enhance AI disponible. Usa el CLI para mas opciones."

        if cmd_lower in ("shield", "escudo", "anti-spam"):
            if not self._shield:
                return "Shield module no disponible"
            stats = self._shield.get_stats()
            return (f"Escudo Anti-Spam:\n"
                    f"  Patrones: {stats['patterns_loaded']}\n"
                    f"  Números bloqueados: {stats['blocked_numbers']}\n"
                    f"  Amenazas detectadas: {stats['threats_detected']}")

        if cmd_lower.startswith("analiza mensaje "):
            msg = cmd[16:].strip()
            if not self._shield:
                return "Shield module no disponible"
            result = self._shield.analyze_message(msg)
            return (f"Score: {result['threat_score']}/100\n"
                    f"Amenaza: {'SÍ' if result['is_scam'] else 'NO'}\n"
                    f"Acción: {result['action']}\n"
                    f"Razones: {', '.join(result['reasons']) or 'Ninguna'}")

        if cmd_lower.startswith("bloquea numero "):
            num = cmd[15:].strip()
            if not self._shield:
                return "Shield module no disponible"
            self._shield.block_number(num, "Bloqueado por usuario")
            return f"Número {num} bloqueado."

        if cmd_lower in ("sentinel", "salud modulos", "heartbeat"):
            if not self._sentinel:
                return "Sentinel no disponible"
            report = self._sentinel.get_health_report()
            lines = ["Heartbeat de módulos:"]
            for name, h in report.items():
                icon = "✓" if h["status"] == "healthy" else "✗"
                lines.append(f"  {icon} {name}: {h['status']} (fallos: {h['consecutive_failures']})")
            return "\n".join(lines)

        if cmd_lower in ("pre-flight", "preflight", "verificar sistema"):
            if not self._pre_flight:
                return "Pre-flight no disponible"
            result = self._pre_flight.run_all()
            lines = [f"Pre-Flight: {result['passed']}/{result['total']} OK"]
            for c in result["checks"]:
                icon = "✓" if c["status"] == "OK" else "⚠" if c["status"] == "WARN" else "✗"
                lines.append(f"  {icon} {c['name']}: {c['detail'] or c['status']}")
            return "\n".join(lines)

        if cmd_lower in ("voice engine", "voz stark", "edge tts"):
            if not self._voice_engine:
                return "Voice Engine no disponible"
            status = self._voice_engine.get_status()
            return (f"Voice Engine (Stark):\n"
                    f"  Voz: {status['voice_id']}\n"
                    f"  Velocidad: {status['rate']}\n"
                    f"  Tono: {status['pitch']}\n"
                    f"  Cola: {status['queue_size']} mensajes")

        if cmd_lower.startswith("dice "):
            text = cmd[5:].strip()
            if not self._voice_engine:
                return "Voice Engine no disponible"
            self._voice_engine.speak(text)
            return f"Diciendo: {text}"

        if cmd_lower in ("historial parches", "patch history"):
            if not self._auto_patcher:
                return "Auto-patcher no disponible"
            history = self._auto_patcher.get_history(20)
            return "\n".join(history) if history else "Sin historial de parches"

        if cmd_lower in ("hola", "buenos dias", "buenas tardes", "buenas noches", "hey", "hello"):
            return "Hola, soy JARVIS. Tus modulos estan listos. Escribe 'status' para verlos o 'ayuda' para comandos."

        if cmd_lower in ("ayuda", "help", "comandos"):
            return ("Comandos disponibles:\n"
                    "  status, sistema, plataforma, heartbeat\n"
                    "  que sabes, aprender, recuerda, olvida\n"
                    "  conversaciones, temas\n"
                    "  busca archivo <nombre>, busca imagen <ruta>, duplicados\n"
                    "  reparar, web on/off, voz on/off/test\n"
                    "  swapface swap <img1> <img2>\n"
                    "  silenciar / mute, activar microfono / unmute\n"
                    "  reconocer, registrar rostro, comparar rostros\n"
                    "  buscar <consulta>, aprende de <url>, ia <pregunta>\n"
                    "  analiza, explica, traduce, genera codigo\n"
                    "  abre <app/web>, busca <texto> [en <sitio>]\n"
                    "  click, doble click, escribe <texto>, presiona <tecla>\n"
                    "  abre youtube, reproduce <video>, captura\n"
                    "  apagar, reiniciar, bloquear, suspender\n"
                    "  instala <paquete>, toma foto, graba video\n"
                    "  shield, analiza mensaje <msg>, bloquea numero <num>\n"
                    "  dice <texto>, voice engine, historial parches\n"
                    "  pre-flight, sentinel\n"
                    "  hola, ayuda, salir")

        if cmd_lower in ("vpn", "vpn status", "cluster", "cluster status"):
            lines = []
            if self._vpn:
                s = self._vpn.get_status()
                lines.append(f"VPN Bridge: activo ({s['encryption']})")
                lines.append(f"  Tunnels activos: {s['sessions']}")
                for t in s['active_tunnels']:
                    lines.append(f"    - {t['node_name']} ({t['node_id']}) uptime: {t['uptime']}s")
                lines.append(f"  CPU local: {s['local_cpu']}%")
            else:
                lines.append("VPN Bridge: DESACTIVADO")
            if self._mesh:
                info = self._mesh.get_status()
                lines.append(f"Mesh Cluster: activo ({len(info['nodes'])} nodos)")
                for n in info['nodes']:
                    lines.append(f"  - {n['name']} alive={n['alive']} cpu={n['cpu']}%")
            else:
                lines.append("Mesh Cluster: DESACTIVADO")
            return "\n".join(lines)

        if cmd_lower.startswith("swapface ") and self._mesh and self._vpn:
            self.logger.info("[DELEGACION] swapface detectado — verificando CPU para delegacion...")
            try:
                import psutil
                if psutil.cpu_percent(interval=0.2) > 80:
                    self.logger.info("[DELEGACION] CPU alta — delegando swapface via VPN...")
                    targets = [n for n in self._mesh.nodes if n.get("alive")]
                    if targets:
                        result = self._vpn.send_task(targets[0]["name"], "swapface", {"cmd": cmd})
                        if result and result.get("status") == "completed":
                            return f"[DELEGADO a {targets[0]['name']}] {result['result']}"
            except Exception:
                pass

        if self.system_controller:
            result = self.system_controller.process_command(cmd)
            if result is not None:
                return result

        try:
            from core.command_router import execute_command as router_fn
            rr = router_fn(cmd)
            if not rr.startswith("Comando no soportado"):
                return rr
        except Exception:
            pass

        return f"Comando no reconocido: '{cmd}'. Escribe 'ayuda' para ver los comandos disponibles."

    # ==========================================
    # CLI LOOP
    # ==========================================

    def cli_loop(self):
        while True:
            try:
                cmd = input("Jarvis > ")
                cmd_lower = cmd.lower().strip()

                if cmd_lower in ("salir", "exit", "cerrar", "apagar jarvis"):
                    self.logger.info("Cerrando Jarvis...")
                    print("Jarvis apagado.")
                    break

                if cmd_lower.startswith("genera codigo") and self._code_analyzer:
                    parts = cmd.split(None, 2)
                    if len(parts) >= 3:
                        lenguaje = parts[2].lower()
                        desc = input("Describe el codigo que quieres generar: ")
                        res = self._code_analyzer.generar_codigo(desc, lenguaje)
                        if res.get("ok"):
                            print(f"\n--- Codigo {lenguaje.upper()} generado ---")
                            print(res['codigo'])
                        else:
                            print(f"Error: {res.get('error', 'No se pudo generar')}")
                    else:
                        print("Uso: genera codigo <lenguaje>")
                        print("Te pedire la descripcion a continuacion.")
                    continue

                result = self.process_command(cmd)
                print(result)
                if self.jarvis_brain and cmd_lower not in (
                    "salir", "exit", "cerrar", "apagar jarvis",
                    "hola", "ayuda", "help", "comandos", "status"
                ):
                    if not cmd_lower.startswith("aprender "):
                        self.jarvis_brain.record_conversation(cmd, result)

            except KeyboardInterrupt:
                self.logger.warning("Interrupcion manual detectada.")
                print("\nJarvis detenido.")
                break
            except Exception as error:
                self.error_manager.handle_error(error, "MAIN_LOOP")
                print("Ocurrio un error, pero Jarvis sigue estable.")
