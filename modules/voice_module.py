# ==========================================
# JARVIS VOICE MODULE
# modules/voice_module.py
# ==========================================

import speech_recognition as sr

class VoiceModule:

    def __init__(self):

        self.engine = None

        try:
            import pyttsx3
            self.engine = pyttsx3.init()

            voices = self.engine.getProperty('voices')

            if voices:
                self.engine.setProperty('voice', voices[0].id)

            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 1.0)

            print("[VOICE] Motor de voz cargado.")

        except Exception as e:
            print("[VOICE ERROR]", e)
            print("[VOICE] Ejecutando sin voz TTS.")

    def speak(self, text):
        print(f"Jarvis: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print("[VOICE SPEAK ERROR]", e)

    def listen(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 1.2

        try:
            with sr.Microphone() as source:
                print("\nEscuchando...\n")
                recognizer.adjust_for_ambient_noise(source, duration=2)
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)

            command = recognizer.recognize_google(audio, language="es-MX")
            print(f"Tú dijiste: {command}")
            return command.lower()

        except sr.WaitTimeoutError:
            print("[LISTEN] Nadie habló.")
            return ""
        except sr.UnknownValueError:
            print("[LISTEN] No entendí.")
            return ""
        except sr.RequestError:
            print("[LISTEN] Sin internet.")
            return ""
        except Exception as e:
            print("[LISTEN ERROR]", e)
            return ""