# ==========================================
# APP MODULE
# modules/app_module.py
# ==========================================

import os

class AppModule:

    def open_brave(self):
        print("[APP] Abriendo Brave")
        os.system('cmd /c start brave')

    def open_calculator(self):
        print("[APP] Abriendo Calculadora")
        os.system('cmd /c start calc')

    def open_notepad(self):
        print("[APP] Abriendo Bloc de Notas")
        os.system('cmd /c start notepad')

    def open_vscode(self):
        print("[APP] Abriendo Visual Studio Code")
        os.system('cmd /c start code')