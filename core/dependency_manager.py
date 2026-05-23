import subprocess
import sys

from core.logger import JarvisLogger


class DependencyManager:

    def __init__(self):

        self.logger = JarvisLogger()

    def install(self, package_name):

        try:

            self.logger.info(
                f"Instalando dependencia: {package_name}"
            )

            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                package_name
            ])

            self.logger.info(
                f"Dependencia instalada: {package_name}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Error instalando {package_name}: {error}"
            )

            return False