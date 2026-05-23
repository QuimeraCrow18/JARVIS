import customtkinter as ctk
import psutil
import threading
import time

# ==========================================
# CONFIGURACIÓN BASE
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# VENTANA PRINCIPAL
# ==========================================

class JarvisUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("JARVIS")
        self.geometry("1200x700")

        self.configure(fg_color="#050816")

        # ==================================
        # PANEL IZQUIERDO
        # ==================================

        self.left_panel = ctk.CTkFrame(
            self,
            width=250,
            fg_color="#0A0F1F",
            corner_radius=0
        )

        self.left_panel.pack(side="left", fill="y")

        # ==================================
        # TÍTULO
        # ==================================

        self.title_label = ctk.CTkLabel(
            self.left_panel,
            text="JARVIS",
            font=("Consolas", 32, "bold"),
            text_color="#00D9FF"
        )

        self.title_label.pack(pady=30)

        # ==================================
        # ESTADO
        # ==================================

        self.status_label = ctk.CTkLabel(
            self.left_panel,
            text="Sistema estable",
            font=("Consolas", 16),
            text_color="#00FF99"
        )

        self.status_label.pack(pady=10)

        # ==================================
        # CPU
        # ==================================

        self.cpu_label = ctk.CTkLabel(
            self.left_panel,
            text="CPU: 0%",
            font=("Consolas", 15)
        )

        self.cpu_label.pack(pady=10)

        self.cpu_bar = ctk.CTkProgressBar(
            self.left_panel,
            width=180
        )

        self.cpu_bar.pack(pady=5)

        # ==================================
        # RAM
        # ==================================

        self.ram_label = ctk.CTkLabel(
            self.left_panel,
            text="RAM: 0%",
            font=("Consolas", 15)
        )

        self.ram_label.pack(pady=10)

        self.ram_bar = ctk.CTkProgressBar(
            self.left_panel,
            width=180
        )

        self.ram_bar.pack(pady=5)

        # ==================================
        # PANEL CENTRAL
        # ==================================

        self.center_panel = ctk.CTkFrame(
            self,
            fg_color="#081120"
        )

        self.center_panel.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================
        # TERMINAL VISUAL
        # ==================================

        self.console = ctk.CTkTextbox(
            self.center_panel,
            font=("Consolas", 14),
            fg_color="#02050D",
            text_color="#00FFCC"
        )

        self.console.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.log("JARVIS ONLINE")
        self.log("Sistema iniciado correctamente.")
        self.log("Autorepair activo.")
        self.log("SafeLoader activo.")
        self.log("Modo modular activo.")

        # ==================================
        # HILO DE MONITOREO
        # ==================================

        thread = threading.Thread(
            target=self.update_stats,
            daemon=True
        )

        thread.start()

    # ======================================
    # LOG VISUAL
    # ======================================

    def log(self, message):

        current_time = time.strftime("%H:%M:%S")

        self.console.insert(
            "end",
            f"[{current_time}] {message}\n"
        )

        self.console.see("end")

    # ======================================
    # ACTUALIZAR ESTADÍSTICAS
    # ======================================

    def update_stats(self):

        while True:

            cpu = psutil.cpu_percent()

            ram = psutil.virtual_memory().percent

            self.cpu_label.configure(
                text=f"CPU: {cpu}%"
            )

            self.cpu_bar.set(cpu / 100)

            self.ram_label.configure(
                text=f"RAM: {ram}%"
            )

            self.ram_bar.set(ram / 100)

            time.sleep(1)

# ==========================================
# INICIAR UI
# ==========================================

def start_ui():

    app = JarvisUI()

    app.mainloop()