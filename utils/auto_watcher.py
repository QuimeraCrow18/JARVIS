import sys
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MODULES_DIR = "modules"
AUTO_SCRIPT = os.path.join("utils", "autoregistrar.py")

class ModsHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py"):
            print(f"[WATCHDOG] Cambio detectado en {event.src_path}, actualizando main.py...")
            try:
                subprocess.run([sys.executable, AUTO_SCRIPT], check=True)
                print("[WATCHDOG] main.py actualizado (imports refrescados).")
            except Exception as e:
                print(f"[WATCHDOG] Error al auto-registrar: {e}")

def run_watcher():
    event_handler = ModsHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MODULES_DIR, recursive=False)
    observer.start()
    print("[WATCHDOG] Observando cambios en /modules/. Presiona Ctrl+C para salir.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    run_watcher()