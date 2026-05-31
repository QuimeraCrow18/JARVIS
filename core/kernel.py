# =========================================
# JARVIS AI SYSTEM
# kernel.py
# =========================================

from core.module_loader import ModuleLoader
from core.event_bus import EventBus


class JarvisKernel:

    def __init__(self):

        self.system_name = "JARVIS"
        self.version = "0.0.1"
        self.status = "OFFLINE"

        # SYSTEMS
        self.module_loader = ModuleLoader()
        self.event_bus = EventBus()

    def boot(self):

        self.status = "ONLINE"

        print(f"{self.system_name} Kernel Booting...")
        print(f"Version: {self.version}")
        print(f"Status: {self.status}")

    def load_core_modules(self):

        self.module_loader.load_module("voice.voice")
        self.module_loader.load_module("modules.memory_module")
        self.module_loader.load_module("modules.voice_module")
        self.module_loader.load_module("modules.media_module")

    def show_loaded_modules(self):

        self.module_loader.show_modules()

    def emit_event(self, event_name, data=None):

        self.event_bus.emit(event_name, data)