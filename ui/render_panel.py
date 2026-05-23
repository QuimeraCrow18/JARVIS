import customtkinter as ctk
from tkinter import ttk
import threading
import time

class RenderPanelUI:
    def __init__(self, title="Previsualización de Video"):
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry("500x200")
        self.root.resizable(False, False)

        # Barra de progreso
        self.progress_label = ctk.CTkLabel(self.root, text="Progreso:")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.root, length=400)
        self.progress_bar.pack(pady=5)

        # Estado de render
        self.status_label = ctk.CTkLabel(self.root, text="Esperando archivo...")
        self.status_label.pack(pady=10)

        # Bloqueo para hilos
        self._lock = threading.Lock()
        threading.Thread(target=self.root.mainloop, daemon=True).start()

    def update_progress(self, value, max_value=100):
        with self._lock:
            percent = int((value / max_value) * 100)
            self.progress_bar['value'] = percent
            self.status_label.configure(text=f"Procesando... {percent}%")
            self.root.update_idletasks()

    def set_status(self, text):
        with self._lock:
            self.status_label.configure(text=text)
            self.root.update_idletasks()