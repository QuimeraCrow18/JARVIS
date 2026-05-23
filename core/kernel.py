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

        self.module_loader.load_module("voice_system")
        self.module_loader.load_module("memory_system")
        self.module_loader.load_module("device_analyzer")
        self.module_loader.load_module("optimizer")

    def show_loaded_modules(self):

        self.module_loader.show_modules()

    def emit_event(self, event_name, data=None):

        self.event_bus.emit(event_name, data)