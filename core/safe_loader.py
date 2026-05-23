import importlib

from core.logger import JarvisLogger
from core.error_manager import ErrorManager


class SafeLoader:

    def __init__(self):

        self.logger = JarvisLogger()
        self.error_manager = ErrorManager()

    def load_module(self, module_path):

        try:

            module = importlib.import_module(module_path)

            self.logger.info(
                f"Módulo cargado: {module_path}"
            )

            return module

        except Exception as error:

            self.error_manager.handle_error(
                error,
                module_path
            )

            self.logger.warning(
                f"Módulo desactivado: {module_path}"
            )

            return None