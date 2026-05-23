# =========================================
# JARVIS - SYSTEM MANAGER
# =========================================

class SystemManager:

    def __init__(self):
        self.system_status = "ONLINE"
        self.active_modules = []
        self.errors = []

    def register_module(self, module_name):
        if module_name not in self.active_modules:
            self.active_modules.append(module_name)
            print(f"[SYSTEM] Módulo registrado: {module_name}")

    def remove_module(self, module_name):
        if module_name in self.active_modules:
            self.active_modules.remove(module_name)
            print(f"[SYSTEM] Módulo removido: {module_name}")

    def show_modules(self):
        print("\n=== MODULOS ACTIVOS ===")

        for module in self.active_modules:
            print(f"-> {module}")

    def add_error(self, error):
        self.errors.append(error)

    def show_errors(self):
        print("\n=== ERRORES ===")

        for error in self.errors:
            print(error)

    def get_status(self):
        return self.system_status