import customtkinter as ctk
import threading
import time
import math
import os
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ANCHO = 600
ALTO = 400
DURACION = 2.5

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._destroyed = False
        self._start_time = time.time()

        if parent:
            self.transient(parent)
        self.overrideredirect(True)

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = (ancho_pantalla - ANCHO) // 2
        y = (alto_pantalla - ALTO) // 2
        self.geometry(f"{ANCHO}x{ALTO}+{x}+{y}")

        self.configure(fg_color="#050816")
        self.attributes("-topmost", True)
        self.lift()

        self.canvas = ctk.CTkCanvas(
            self,
            width=ANCHO,
            height=ALTO,
            bg="#050816",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self._init_draw()

        self._animacion_activa = True
        threading.Thread(target=self._animar, daemon=True).start()

    def _init_draw(self):
        cx, cy = ANCHO // 2, ALTO // 2 - 30
        self.canvas.create_text(
            cx, 50,
            text="JARVIS",
            font=("Consolas", 48, "bold"),
            fill="#00D9FF",
            tags="titulo"
        )
        self.canvas.create_text(
            cx, 90,
            text="Just A Rather Very Intelligent System",
            font=("Consolas", 10),
            fill="#446688",
            tags="subtitulo"
        )
        self.canvas.create_text(
            cx, ALTO - 40,
            text="v6.0 · Multi-Platform",
            font=("Consolas", 9),
            fill="#334455",
            tags="version"
        )
        for i in range(6):
            angulo = i * (2 * math.pi / 6) - math.pi / 2
            x1 = cx + 80 * math.cos(angulo) - 6
            y1 = cy + 80 * math.sin(angulo) - 6
            x2 = cx + 80 * math.cos(angulo) + 6
            y2 = cy + 80 * math.sin(angulo) + 6
            self.canvas.create_oval(
                x1, y1, x2, y2,
                outline="#00D9FF",
                width=1.5,
                tags=f"orb{i}"
            )
            self.canvas.create_line(
                cx, cy,
                cx + 80 * math.cos(angulo),
                cy + 80 * math.sin(angulo),
                fill="#0A2A4A",
                width=1,
                tags=f"linea{i}"
            )
        self.canvas.create_oval(
            cx - 12, cy - 12, cx + 12, cy + 12,
            fill="#00D9FF",
            outline="#00D9FF",
            tags="nucleo"
        )
        self.canvas.create_text(
            cx, cy,
            text="INIT",
            font=("Consolas", 8, "bold"),
            fill="#050816",
            tags="init_text"
        )

    def _animar(self):
        cx, cy = ANCHO // 2, ALTO // 2 - 30
        estados = [
            "INIT", "BOOT", "LOAD", "SCAN",
            "SYNC", "AUTH", "ONLINE"
        ]
        paso = 0
        ultimo_cambio = time.time()

        while self._animacion_activa and not self._destroyed:
            elapsed = time.time() - self._start_time

            try:
                progreso = min(elapsed / DURACION, 1.0)
                ang_offset = progreso * 2 * math.pi

                for i in range(6):
                    angulo = i * (2 * math.pi / 6) - math.pi / 2 + ang_offset
                    x = cx + 80 * math.cos(angulo)
                    y = cy + 80 * math.sin(angulo)

                    brillo = int(100 + 155 * (0.5 + 0.5 * math.sin(ang_offset - i)))
                    color = f"#{brillo:02x}{brillo:02x}FF"

                    self.canvas.itemconfig(f"orb{i}", fill=color, outline=color)
                    self.canvas.itemconfig(f"linea{i}", fill=f"#{brillo//3:02x}2A4A")

                alpha = int(200 + 55 * (0.5 + 0.5 * math.sin(ang_offset * 2)))
                nucleo = f"#{alpha:02x}{alpha:02x}FF"
                self.canvas.itemconfig("nucleo", fill=nucleo, outline=nucleo)

                if time.time() - ultimo_cambio > 0.35:
                    paso = (paso + 1) % len(estados)
                    self.canvas.itemconfig("init_text", text=estados[paso])
                    ultimo_cambio = time.time()

                if progreso >= 1.0:
                    self.canvas.itemconfig("init_text", text="ONLINE")
                    self.canvas.itemconfig("titulo", fill="#00FF88")

                if not self._destroyed:
                    self.update_idletasks()
                time.sleep(0.03)

            except Exception:
                break

    def close(self):
        self._animacion_activa = False
        self._destroyed = True
        try:
            self.withdraw()
            self.destroy()
        except Exception:
            pass


def show_splash(parent=None, duracion=None):
    splash = SplashScreen(parent)
    if duracion:
        time.sleep(duracion)
    return splash


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()

    splash = SplashScreen(root)
    splash.after(int(DURACION * 1000) + 500, lambda: [splash.close(), root.destroy()])
    root.mainloop()
