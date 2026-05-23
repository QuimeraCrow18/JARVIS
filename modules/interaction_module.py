# ==========================================
# INTERACTION MODULE
# modules/interaction_module.py
# ==========================================

import time


class InteractionModule:

    def __init__(self):

        print("[INTERACTION] Módulo iniciado.")

        self.pyautogui = None

        try:

            import pyautogui

            self.pyautogui = pyautogui

            print("[INTERACTION] PyAutoGUI cargado.")

        except Exception as e:

            print("[INTERACTION ERROR]", e)
            print("[INTERACTION] Ejecutando sin automatización.")

    # ==========================================
    # CLICK
    # ==========================================

    def click(self, x=None, y=None):

        if not self.pyautogui:
            return False

        try:

            if x is not None and y is not None:

                self.pyautogui.click(x, y)

            else:

                self.pyautogui.click()

            return True

        except Exception as e:

            print("[CLICK ERROR]", e)
            return False

    # ==========================================
    # DOBLE CLICK
    # ==========================================

    def double_click(self):

        if not self.pyautogui:
            return False

        try:

            self.pyautogui.doubleClick()

            return True

        except Exception as e:

            print("[DOUBLE CLICK ERROR]", e)
            return False

    # ==========================================
    # ESCRIBIR TEXTO
    # ==========================================

    def write_text(self, text):

        if not self.pyautogui:
            return False

        try:

            self.pyautogui.write(
                text,
                interval=0.05
            )

            return True

        except Exception as e:

            print("[WRITE ERROR]", e)
            return False

    # ==========================================
    # PRESIONAR TECLA
    # ==========================================

    def press_key(self, key):

        if not self.pyautogui:
            return False

        try:

            self.pyautogui.press(key)

            return True

        except Exception as e:

            print("[KEY ERROR]", e)
            return False

    # ==========================================
    # COMBINACIÓN DE TECLAS
    # ==========================================

    def hotkey(self, *keys):

        if not self.pyautogui:
            return False

        try:

            self.pyautogui.hotkey(*keys)

            return True

        except Exception as e:

            print("[HOTKEY ERROR]", e)
            return False

    # ==========================================
    # MOVER MOUSE
    # ==========================================

    def move_mouse(self, x, y):

        if not self.pyautogui:
            return False

        try:

            self.pyautogui.moveTo(
                x,
                y,
                duration=0.5
            )

            return True

        except Exception as e:

            print("[MOVE ERROR]", e)
            return False

    # ==========================================
    # SCROLL
    # ==========================================

    def scroll(self, amount):

        if not self.pyautogui:
            return False

        try:

            self.pyautogui.scroll(amount)

            return True

        except Exception as e:

            print("[SCROLL ERROR]", e)
            return False