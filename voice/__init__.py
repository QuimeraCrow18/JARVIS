# =========================================
# JARVIS - VOICE MODULE
# =========================================

import pyttsx3


class VoiceSystem:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 170)

    def speak(self, text):

        print(f"[JARVIS VOICE]: {text}")

        self.engine.say(text)
        self.engine.runAndWait()