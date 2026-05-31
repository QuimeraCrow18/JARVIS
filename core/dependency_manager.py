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

            proc = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                timeout=60,
                capture_output=True,
                text=True
            )

            if proc.returncode == 0:

                self.logger.info(
                    f"Dependencia instalada: {package_name}"
                )

                return True

            else:

                self.logger.warning(
                    f"Fallo al instalar {package_name}: {proc.stderr[:200]}"
                )

                return False

        except subprocess.TimeoutExpired:

            self.logger.warning(
                f"Timeout instalando {package_name}"
            )

            return False

        except Exception as error:

            self.logger.error(
                f"Error instalando {package_name}: {error}"
            )

            return False