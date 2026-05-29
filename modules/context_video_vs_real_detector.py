# ==========================================
# CONTEXT VIDEO VS REAL ACTION DETECTOR
# Distingue entre VIDEO/PELÍCULA y ACCIÓN REAL
# modules/context_video_vs_real_detector.py
# ==========================================

from core.utils import safe_method
from datetime import datetime
import os

class ContextVideoVsRealDetector:
    def __init__(self):
        print("[CONTEXT-DETECTOR] Detector de contexto (video vs real) iniciado")
        
        self.is_media_playing = False
        self.current_app = None
        self.audio_source = None
        self.context_type = None
        self.confidence = 0

    @safe_method
    def detect_if_video_playing(self):
        """
        Detecta si hay un video/película/serie reproduciéndose
        """
        print("[CONTEXT-DETECTOR] 🎬 DETECTANDO SI HAY VIDEO REPRODUCIENDO")
        
        # En Android: comprobaría si apps como YouTube, Netflix, películas están activas
        # En Windows: comprobaría si hay reproductor de video activo
        
        video_apps = [
            "Netflix",
            "YouTube",
            "Amazon Prime Video",
            "Disney+",
            "HBO Max",
            "Twitch",
            "VLC",
            "Windows Media Player",
            "Movies",
            "Películas",
            "Reproductor de vídeo"
        ]
        
        # Simulado - en real usaría APIs del SO
        self.current_app = "Netflix"  # Ejemplo simulado
        
        if self.current_app in video_apps:
            self.is_media_playing = True
            print(f"   ✓ APP DE VIDEO DETECTADA: {self.current_app}")
            print(f"   ✓ VIDEO/PELÍCULA EN REPRODUCCIÓN")
            return True
        else:
            self.is_media_playing = False
            print(f"   • App actual: {self.current_app}")
            print(f"   • NO hay video en reproducción")
            return False

    @safe_method
    def analyze_audio_source(self, audio_characteristics):
        """
        Analiza si el audio viene de:
        - MICRÓFONO (persona real hablando)
        - ALTAVOZ (película/video/llamada)
        """
        print("[CONTEXT-DETECTOR] 🔊 ANALIZANDO ORIGEN DEL AUDIO")
        
        # Características típicas de VIDEO/PELÍCULA vs AUDIO REAL
        video_indicators = {
            "background_music": 20,          # Las películas tienen música de fondo
            "sound_effects": 25,             # Efectos de sonido
            "multiple_speakers": 15,         # Diálogos de actores
            "professional_audio": 30,        # Audio mezclado profesionalmente
            "echo_in_audio": 5,              # Audio procesado
            "consistent_volume": 10,         # Volumen normalizado
            "no_ambient_noise": 20,          # Sin ruido ambiente real
            "perfect_clarity": 15,           # Audio muy claro
        }
        
        real_call_indicators = {
            "ambient_noise": 25,             # Ruido de fondo de ambiente real
            "voice_only": 30,                # Solo una voz sin música
            "irregular_volume": 20,          # Volumen variable
            "background_sounds": 20,         # Sonidos reales (tráfico, gente)
            "echo_from_distance": 15,        # Eco natural de larga distancia
            "breathing_sounds": 15,          # Respiración audible
            "emotion_variation": 20,         # Variaciones emocionales reales
        }
        
        video_score = sum(video_indicators.values())  # Simulado
        real_score = sum(real_call_indicators.values())
        
        if video_score > real_score:
            self.audio_source = "VIDEO/PELÍCULA"
            print(f"   ✓ AUDIO DE VIDEO DETECTADO")
            print(f"   ✓ Score video: {video_score}")
            return "VIDEO"
        else:
            self.audio_source = "MICRÓFONO REAL"
            print(f"   ✓ AUDIO DE MICRÓFONO REAL DETECTADO")
            print(f"   ✓ Score real: {real_score}")
            return "REAL"

    @safe_method
    def check_screen_activity_correlation(self):
        """
        Correlaciona audio amenazante con actividad en pantalla:
        - ¿El usuario está viendo una película? → Probablemente video
        - ¿La pantalla está bloqueada? → Probablemente llamada real
        - ¿Se abrió una app inesperadamente? → Podría ser ataque
        """
        print("[CONTEXT-DETECTOR] 📱 ANALIZANDO CORRELACIÓN PANTALLA-AUDIO")
        
        screen_context = {
            "screen_locked": False,
            "app_active": "Netflix",
            "full_screen": True,
            "brightness": 100,
            "recent_app_change": False,
            "gesture_detected": False
        }
        
        # Si la pantalla está bloqueada y hay amenaza = más probable que sea REAL
        if screen_context["screen_locked"] and not self.is_media_playing:
            print("   ✓ Pantalla bloqueada + Sin video = PROBABILIDAD ALTA DE REAL")
            return "LIKELY_REAL"
        
        # Si está viendo una película a pantalla completa = más probable VIDEO
        elif screen_context["full_screen"] and self.is_media_playing:
            print("   ✓ Pantalla completa + Video activo = PROBABILIDAD ALTA DE VIDEO")
            return "LIKELY_VIDEO"
        
        # Si la app cambió de repente = SOSPECHOSO
        elif screen_context["recent_app_change"]:
            print("   ⚠️ Cambio de app inesperado = REQUIERE VERIFICACIÓN")
            return "SUSPICIOUS"
        
        else:
            print("   • Contexto ambiguo = REQUIERE ANÁLISIS ADICIONAL")
            return "AMBIGUOUS"

    @safe_method
    def detect_movie_dialogue_patterns(self, transcript):
        """
        Detecta PATRONES típicos de PELÍCULAS/SERIES:
        - Diálogos muy dramáticos
        - Frases memorables/clichés
        - Guión obvio
        """
        print("[CONTEXT-DETECTOR] 🎭 DETECTANDO PATRONES DE DIÁLOGOS")
        
        movie_clichés = {
            "te voy a matar": 20,          # Muy común en películas
            "escucha bien": 15,
            "tengo un plan": 15,
            "esto no termina aquí": 15,
            "confía en mí": 10,
            "no tienes opción": 15,
            "es hora de ajustar cuentas": 20,
            "recuerdas lo que hiciste": 20,
            "tiempo se acabó": 15,
            "tú y yo tenemos una cuenta pendiente": 25,
            "no volverás a ver": 15,
            "esto es el fin": 15,
        }
        
        real_threat_patterns = {
            "dame tu": 25,                  # Robo: demandas directas
            "tu dinero": 20,
            "ahora mismo": 20,
            "no me hagas daño": 15,
            "tengo acceso a": 20,
            "tu familia": 25,
            "coordenadas": 20,
            "prueba de vida": 20,
        }
        
        transcript_lower = transcript.lower()
        
        movie_score = 0
        real_score = 0
        
        for phrase, weight in movie_clichés.items():
            if phrase in transcript_lower:
                movie_score += weight
        
        for phrase, weight in real_threat_patterns.items():
            if phrase in transcript_lower:
                real_score += weight
        
        print(f"   Movie score: {movie_score}")
        print(f"   Real threat score: {real_score}")
        
        if movie_score > real_score:
            print("   ✓ PATRONES DE PELÍCULA DETECTADOS")
            return "MOVIE_DIALOGUE"
        elif real_score > movie_score:
            print("   ✓ PATRONES DE AMENAZA REAL DETECTADOS")
            return "REAL_THREAT"
        else:
            print("   • Patrones ambiguos")
            return "AMBIGUOUS"

    @safe_method
    def check_user_response_to_threat(self, user_behavior):
        """
        Analiza cómo responde el usuario a la amenaza:
        - ¿Está tranquilo? → Probablemente video
        - ¿Está en pánico? → Probablemente real
        - ¿Sigue mirando? → Probablemente video
        """
        print("[CONTEXT-DETECTOR] 👤 ANALIZANDO COMPORTAMIENTO DEL USUARIO")
        
        if user_behavior.get("stress_level", 0) > 80:
            print("   ✓ Usuario en PÁNICO = PROBABILIDAD ALTA DE REAL")
            return "REAL_THREAT"
        
        if user_behavior.get("continued_watching", False):
            print("   ✓ Usuario sigue mirando = PROBABLEMENTE VIDEO")
            return "LIKELY_VIDEO"
        
        if user_behavior.get("trying_to_escape", False):
            print("   ✓ Usuario intentando escapar = REAL")
            return "REAL_THREAT"
        
        print("   • Comportamiento neutral")
        return "UNCLEAR"

    @safe_method
    def final_context_determination(self, detection_results):
        """
        Análisis FINAL: ¿Es VIDEO o ACCIÓN REAL?
        """
        print("\n[CONTEXT-DETECTOR] 🔍 ANÁLISIS FINAL DE CONTEXTO")
        print("─" * 60)
        
        video_votes = 0
        real_votes = 0
        
        for result in detection_results:
            if result == "VIDEO" or "VIDEO" in result:
                video_votes += 1
            elif result == "REAL" or "REAL" in result:
                real_votes += 1
        
        total_votes = video_votes + real_votes
        
        if total_votes == 0:
            print("   ⚠️ No hay datos suficientes")
            return {
                "context_type": "UNKNOWN",
                "confidence": 0,
                "action": "MANUAL_REVIEW_REQUIRED"
            }
        
        confidence = max(video_votes, real_votes) / total_votes
        
        if video_votes > real_votes:
            context = "VIDEO"
            action = "NO ACTIVAR PROTOCOLOS DE EMERGENCIA"
            print(f"   ✓ CONTEXTO: VIDEO/PELÍCULA")
            print(f"   ✓ Confianza: {confidence*100:.0f}%")
            print(f"   ✓ Acción: {action}")
        elif real_votes > video_votes:
            context = "REAL"
            action = "ACTIVAR PROTOCOLOS DE EMERGENCIA"
            print(f"   ✓ CONTEXTO: ACCIÓN REAL")
            print(f"   ✓ Confianza: {confidence*100:.0f}%")
            print(f"   ✓ Acción: {action}")
        else:
            context = "AMBIGUOUS"
            action = "REQUIERE CONFIRMACIÓN MANUAL"
            print(f"   ⚠️ CONTEXTO: AMBIGUO")
            print(f"   ⚠️ Acción: {action}")
        
        self.context_type = context
        self.confidence = confidence
        
        return {
            "context_type": context,
            "confidence": confidence,
            "action": action,
            "video_votes": video_votes,
            "real_votes": real_votes,
            "should_activate_emergency": real_votes > video_votes
        }

    @safe_method
    def get_context_status(self):
        """Retorna estado del análisis de contexto"""
        return {
            "media_playing": self.is_media_playing,
            "current_app": self.current_app,
            "audio_source": self.audio_source,
            "context_type": self.context_type,
            "confidence": self.confidence,
            "emergency_should_activate": self.context_type == "REAL"
        }