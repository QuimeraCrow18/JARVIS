import customtkinter as ctk
import threading

class TextInputUI:
    def __init__(self, title="JARVIS ONLINE"):
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.voice_enabled = True
        self._command = None

        self.entry = ctk.CTkEntry(self.root, placeholder_text="Escribe un comando...")
        self.entry.pack(pady=10, padx=10, fill="x")

        self.send_button = ctk.CTkButton(self.root, text="Enviar", command=self._send_command)
        self.send_button.pack(pady=5)

        self.mic_button = ctk.CTkButton(self.root, text="Micrófono ACTIVADO", command=self._toggle_voice)
        self.mic_button.pack(pady=5)

        self._lock = threading.Lock()
        threading.Thread(target=self.root.mainloop, daemon=True).start()

    def _send_command(self):
        with self._lock:
            self._command = self.entry.get()
            self.entry.delete(0, "end")

    def get_command(self):
        with self._lock:
            cmd = self._command
            self._command = None
            return cmd

    def update(self):
        pass

    def _toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        self.mic_button.configure(text="Micrófono ACTIVADO" if self.voice_enabled else "Micrófono DESACTIVADO")

    def ask_choice(self, options):
        # placeholder simple, puede reemplazarse por GUI
        choice = input(f"Elige ({'/'.join(options)}): ")
        return choice

    def ask_input(self, prompt):
        return input(prompt)