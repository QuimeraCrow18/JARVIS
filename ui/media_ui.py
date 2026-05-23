import customtkinter as ctk
from tkinter import filedialog
import threading

class MediaUploadUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Media Panel")
        self.root.geometry("400x200")

        self._lock = threading.Lock()
        threading.Thread(target=self.root.mainloop, daemon=True).start()

    def select_files(self, prompt="Selecciona archivos"):
        path = filedialog.askopenfilenames(title=prompt)
        return list(path) if path else []

    def update(self):
        pass