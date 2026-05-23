import os
from datetime import datetime


class JarvisLogger:

    def __init__(self):

        self.log_dir = "logs"

        os.makedirs(self.log_dir, exist_ok=True)

        self.log_file = os.path.join(
            self.log_dir,
            "jarvis.log"
        )

    def log(self, level, message):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_message = f"[{timestamp}] [{level}] {message}"

        print(log_message)

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(log_message + "\n")

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)

    def critical(self, message):
        self.log("CRITICAL", message)