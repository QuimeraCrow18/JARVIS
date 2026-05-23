# =========================================
# JARVIS AI SYSTEM
# module_loader.py
# =========================================


class ModuleLoader:

    def __init__(self):

        self.modules = []

    def load_module(self, module_name):

        self.modules.append(module_name)

        print(f"[MODULE LOADED] {module_name}")

    def show_modules(self):

        print("\nLoaded Modules:")

        for module in self.modules:
            print(f" - {module}")