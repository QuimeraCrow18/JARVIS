from core.logger import JarvisLogger
import traceback


class ErrorManager:

    def __init__(self):

        self.logger = JarvisLogger()

    def handle_error(self, error, module_name="UNKNOWN"):

        error_text = traceback.format_exc()

        self.logger.error(
            f"[{module_name}] {str(error)}"
        )

        self.logger.error(error_text)

        return {
            "module": module_name,
            "error": str(error),
            "traceback": error_text
        }