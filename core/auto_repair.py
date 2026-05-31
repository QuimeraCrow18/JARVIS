import importlib

from core.logger import JarvisLogger
from core.dependency_manager import DependencyManager


class AutoRepair:

    def __init__(self):

        self.logger = JarvisLogger()

        self.dependency_manager = DependencyManager()

        self.required_packages = {
            "cv2": "opencv-python",
            "PIL": "pillow",
            "customtkinter": "customtkinter",
            "numpy": "numpy"
        }

    def check_dependencies(self):

        for module_name, package_name in self.required_packages.items():

            try:

                importlib.import_module(module_name)

                self.logger.info(
                    f"Dependencia OK: {module_name}"
                )

            except Exception:

                self.logger.warning(
                    f"Dependencia no disponible: {module_name}"
                )

                self.dependency_manager.install(package_name)