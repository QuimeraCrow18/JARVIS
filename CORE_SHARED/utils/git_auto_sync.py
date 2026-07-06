# utils/git_auto_sync.py
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoSyncHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_commit_time = 0
        self.commit_delay = 10  # Espera 10 segundos antes de hacer commit
    
    def on_modified(self, event):
        if event.src_path.endswith(('.py', '.txt', '.md', '.json')):
            self.trigger_sync()
    
    def on_created(self, event):
        if event.src_path.endswith(('.py', '.txt', '.md', '.json')):
            self.trigger_sync()
    
    def on_deleted(self, event):
        if event.src_path.endswith(('.py', '.txt', '.md', '.json')):
            self.trigger_sync()
    
    def trigger_sync(self):
        current_time = time.time()
        if current_time - self.last_commit_time > self.commit_delay:
            self.last_commit_time = current_time
            self.do_git_sync()
    
    def do_git_sync(self):
        try:
            # Obtener cambios
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
            
            if result.stdout.strip():  # Si hay cambios
                print("[GIT-AUTO-SYNC] Cambios detectados, sincronizando...")
                
                # Agregar cambios
                subprocess.run(['git', 'add', '.'], 
                             cwd=os.path.dirname(os.path.dirname(__file__)), 
                             check=True)
                
                # Hacer commit
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                subprocess.run(['git', 'commit', '-m', f'Auto-sync: {timestamp}'], 
                             cwd=os.path.dirname(os.path.dirname(__file__)), 
                             check=True)
                
                # Hacer push
                subprocess.run(['git', 'push'], 
                             cwd=os.path.dirname(os.path.dirname(__file__)), 
                             check=True)
                
                print(f"[GIT-AUTO-SYNC] ✅ Sincronizado en {timestamp}")
        
        except Exception as e:
            print(f"[GIT-AUTO-SYNC] ❌ Error: {e}")

if __name__ == "__main__":
    observer = Observer()
    handler = GitAutoSyncHandler()
    observer.schedule(handler, path=".", recursive=True)
    observer.start()
    print("[GIT-AUTO-SYNC] Monitoreo de cambios activo. Presiona Ctrl+C para salir.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()