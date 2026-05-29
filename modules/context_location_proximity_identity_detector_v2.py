# ==========================================
# CONTEXT LOCATION PROXIMITY IDENTITY DETECTOR v2
# VERSIÓN CONSERVADORA - Solo alerta si hay EVIDENCIA CLARA
# Sin contactar policía automáticamente
# modules/context_location_proximity_identity_detector_v2.py
# ==========================================

from core.utils import safe_method
from datetime import datetime

class ContextLocationProximityIdentityDetectorV2:
    def __init__(self):
        print("[CONTEXT-V2] Detector conservador (evita falsas alarmas)")
        
        self.device_location = None
        self.content_source = None
        self.device_proximity = None
        self.user_identity_verified = False
        self.threat_confidence = 0
        self.requires_police = False
        self.alert_level = "NORMAL"

    # ========== PARTE 1: ANÁLISIS DE CONTENIDO MÁS RIGUROSO ==========

    @safe_method
    def analyze_content_source_with_high_confidence(self):
        """
        Análisis RIGUROSO de la fuente de contenido
        Solo marca como "NO VIDEO" si tiene MUY ALTA confianza
        """
        print("\n[ANÁLISIS] 🔍 VERIFICANDO ORIGEN DEL CONTENIDO (RIGUROSO)")
        print("─" * 60)
        
        # Checklist exhaustivo para determinar si ES un video/película
        content_checks = {
            "app_video_abierta": self._check_video_app_open(),           # ¿Netflix, YouTube abierto?
            "streaming_activo": self._check_streaming_active(),           # ¿Hay datos de streaming?
            "pantalla_completa_video": self._check_fullscreen_video(),   # ¿Pantalla completa?
            "audio_procesado": self._check_audio_professionally_edited(), # ¿Audio profesional?
            "patrones_movie": self._check_movie_dialogue_patterns(),     # ¿Frases de película?
            "musica_fondo": self._check_background_music(),             # ¿Hay música de fondo?
            "efectos_sonido": self._check_sound_effects(),              # ¿Efectos especiales?
        }
        
        video_confidence = sum(content_checks.values()) / len(content_checks)
        
        print(f"\n   Confianza de que ES video: {video_confidence*100:.0f}%")
        
        if video_confidence > 0.70:  # Solo si >70% confianza
            print(f"   ✓ CLASIFICADO COMO: VIDEO/PELÍCULA/SERIE/ANIME")
            return {
                "is_video": True,
                "confidence": video_confidence,
                "checks_passed": sum(1 for v in content_checks.values() if v > 0.5)
            }
        elif video_confidence > 0.50:
            print(f"   ⚠️ AMBIGUO: Podría ser video (50-70%)")
            return {
                "is_video": True,  # Asumir video por seguridad
                "confidence": video_confidence,
                "checks_passed": sum(1 for v in content_checks.values() if v > 0.5)
            }
        else:
            print(f"   🚨 NO ES VIDEO: Probablemente es contenido real ({video_confidence*100:.0f}%)")
            return {
                "is_video": False,
                "confidence": video_confidence,
                "checks_passed": sum(1 for v in content_checks.values() if v > 0.5)
            }

    @safe_method
    def _check_video_app_open(self):
        """¿Hay app de video abierta?"""
        print("   • ¿Netflix/YouTube abierto?", end=" ")
        result = False  # Simulado
        print(f"→ {result}")
        return 0.85 if result else 0.0

    @safe_method
    def _check_streaming_active(self):
        """¿Hay tráfico de streaming?"""
        print("   • ¿Streaming activo?", end=" ")
        result = False
        print(f"→ {result}")
        return 0.80 if result else 0.0

    @safe_method
    def _check_fullscreen_video(self):
        """¿Pantalla en modo video?"""
        print("   • ¿Pantalla completa?", end=" ")
        result = False
        print(f"→ {result}")
        return 0.70 if result else 0.0

    @safe_method
    def _check_audio_professionally_edited(self):
        """¿Audio procesado profesionalmente?"""
        print("   • ¿Audio profesional?", end=" ")
        result = False
        print(f"→ {result}")
        return 0.75 if result else 0.0

    @safe_method
    def _check_movie_dialogue_patterns(self):
        """¿Patrones de diálogo de película?"""
        print("   • ¿Patrones de película?", end=" ")
        result = False
        print(f"→ {result}")
        return 0.80 if result else 0.0

    @safe_method
    def _check_background_music(self):
        """¿Hay música de fondo?"""
        print("   • ¿Música de fondo?", end=" ")
        result = False
        print(f"→ {result}")
        return 0.70 if result else 0.0

    @safe_method
    def _check_sound_effects(self):
        """¿Hay efectos de sonido?"""
        print("   • ¿Efectos de sonido?", end=" ")
        result = False
        print(f"→ {result}")
        return 0.75 if result else 0.0

    # ========== PARTE 2: PROXIMIDAD MÁS PRECISA ==========

    @safe_method
    def verify_device_actually_away(self):
        """
        Verifica si el dispositivo REALMENTE está lejos del usuario
        No solo "podría estar lejos"
        """
        print("\n[PROXIMIDAD] 📱 VERIFICANDO SI DISPOSITIVO ESTÁ REALMENTE LEJOS")
        print("─" * 60)
        
        proximity_checks = {
            "sensor_proximidad": self._check_proximity_sensor(),      # Sensor infrarrojo
            "acelerometro": self._check_accelerometer(),              # ¿Se está moviendo?
            "gps_distancia": self._check_gps_distance(),              # ¿GPS dice que está lejos?
            "bluetooth_distancia": self._check_bluetooth_distance(),  # Distancia Bluetooth
            "luz_sensor": self._check_light_sensor(),                 # ¿Está oscuro (bolsillo)?
        }
        
        away_confidence = sum(proximity_checks.values()) / len(proximity_checks)
        
        print(f"\n   Confianza de que está LEJOS: {away_confidence*100:.0f}%")
        
        if away_confidence > 0.75:
            print(f"   🚨 DISPOSITIVO REALMENTE ALEJADO (>75% confianza)")
            return {
                "is_away": True,
                "confidence": away_confidence,
                "checks_passed": sum(1 for v in proximity_checks.values() if v > 0.5)
            }
        elif away_confidence > 0.50:
            print(f"   ⚠️ PODRÍA ESTAR LEJOS (50-75%)")
            return {
                "is_away": False,  # No asumir peligro sin confirmación
                "confidence": away_confidence,
                "checks_passed": sum(1 for v in proximity_checks.values() if v > 0.5)
            }
        else:
            print(f"   ✓ DISPOSITIVO PROBABLEMENTE CERCA (<50%)")
            return {
                "is_away": False,
                "confidence": away_confidence,
                "checks_passed": sum(1 for v in proximity_checks.values() if v > 0.5)
            }

    @safe_method
    def _check_proximity_sensor(self):
        print("   • Sensor de proximidad:", end=" ")
        result = False
        print(f"→ {result}")
        return 0.85 if result else 0.0

    @safe_method
    def _check_accelerometer(self):
        print("   • Acelerómetro (movimiento):", end=" ")
        result = False
        print(f"→ {result}")
        return 0.70 if result else 0.0

    @safe_method
    def _check_gps_distance(self):
        print("   • GPS distancia:", end=" ")
        result = False
        print(f"→ {result}")
        return 0.75 if result else 0.0

    @safe_method
    def _check_bluetooth_distance(self):
        print("   • Bluetooth RSSI:", end=" ")
        result = False
        print(f"→ {result}")
        return 0.65 if result else 0.0

    @safe_method
    def _check_light_sensor(self):
        print("   • Luz ambiente:", end=" ")
        result = False
        print(f"→ {result}")
        return 0.60 if result else 0.0

    # ========== PARTE 3: IDENTIDAD CON BIOMETRÍA MÚLTIPLE ==========

    @safe_method
    def verify_identity_with_multiple_factors(self, user_reference_data):
        """
        Verifica identidad usando MÚLTIPLES factores biométricos
        No solo reconocimiento facial
        """
        print("\n[IDENTIDAD] 🆔 VERIFICACIÓN MULTI-FACTOR DE IDENTIDAD")
        print("─" * 60)
        
        identity_checks = {
            "facial_recognition": self._check_facial_recognition(user_reference_data),
            "voice_recognition": self._check_voice_recognition(user_reference_data),
            "fingerprint": self._check_fingerprint(user_reference_data),
            "behavioral_pattern": self._check_behavioral_pattern(),
            "device_unlock_history": self._check_unlock_history(),
        }
        
        identity_confidence = sum(identity_checks.values()) / len(identity_checks)
        
        print(f"\n   Confianza de que ES el usuario: {identity_confidence*100:.0f}%")
        
        if identity_confidence > 0.80:
            print(f"   ✓ VERIFICADO: ES EL USUARIO (>80% confianza)")
            return {
                "is_user": True,
                "confidence": identity_confidence,
                "checks_passed": sum(1 for v in identity_checks.values() if v > 0.5)
            }
        elif identity_confidence > 0.60:
            print(f"   ⚠️ PROBABLEMENTE ES EL USUARIO (60-80%)")
            return {
                "is_user": True,  # Asumir usuario por seguridad
                "confidence": identity_confidence,
                "checks_passed": sum(1 for v in identity_checks.values() if v > 0.5)
            }
        else:
            print(f"   🚨 NO VERIFICADO: NO ES EL USUARIO (<60%)")
            return {
                "is_user": False,
                "confidence": identity_confidence,
                "checks_passed": sum(1 for v in identity_checks.values() if v > 0.5)
            }

    @safe_method
    def _check_facial_recognition(self, user_ref):
        print("   • Reconocimiento facial:", end=" ")
        similarity = 5  # Simulado: 5% (no es el usuario)
        passed = similarity > 85
        print(f"{similarity}% → {passed}")
        return 0.85 if passed else 0.0

    @safe_method
    def _check_voice_recognition(self, user_ref):
        print("   • Reconocimiento de voz:", end=" ")
        similarity = 0  # No hay voz
        passed = False
        print(f"→ {passed}")
        return 0.70 if passed else 0.0

    @safe_method
    def _check_fingerprint(self, user_ref):
        print("   • Huella dactilar:", end=" ")
        verified = False  # No verificado
        print(f"→ {verified}")
        return 0.80 if verified else 0.0

    @safe_method
    def _check_behavioral_pattern(self):
        print("   • Patrón de comportamiento:", end=" ")
        matches = False  # Comportamiento anormal
        print(f"→ {matches}")
        return 0.65 if matches else 0.0

    @safe_method
    def _check_unlock_history(self):
        print("   • Historial de desbloqueo:", end=" ")
        normal = False  # Desbloqueo sospechoso
        print(f"→ {normal}")
        return 0.60 if normal else 0.0

    # ========== PARTE 4: DECISIÓN CONSERVADORA ==========

    @safe_method
    def make_conservative_decision(self, content_result, proximity_result, identity_result):
        """
        DECISIÓN MUY CONSERVADORA
        
        SOLO ACTIVA ALARMA si:
        1. SEGURO que NO es video (>80% confianza)
        2. SEGURO que dispositivo está lejos (>80% confianza)
        3. SEGURO que NO es el usuario (>80% confianza)
        
        NUNCA contacta policía automáticamente
        """
        print("\n" + "="*80)
        print("[DECISIÓN CONSERVADORA] ⚖️ ANÁLISIS FINAL")
        print("="*80)
        
        print("\n📊 FACTORES:")
        print(f"   1. ¿NO es video? {content_result['is_video']*100 if isinstance(content_result['is_video'], float) else (0 if content_result['is_video'] else 100)}% confianza")
        print(f"   2. ¿Dispositivo alejado? {proximity_result['is_away']*100 if isinstance(proximity_result['is_away'], float) else (0 if proximity_result['is_away'] else 100)}% confianza")
        print(f"   3. ¿NO es el usuario? {identity_result['is_user']*100 if isinstance(identity_result['is_user'], float) else (0 if identity_result['is_user'] else 100)}% confianza")
        
        # Lógica CONSERVADORA
        conditions_met = []
        
        # Condición 1: NO es video (confianza >80%)
        if not content_result['is_video'] and content_result['confidence'] > 0.80:
            conditions_met.append("✓ NO es video (>80%)")
        
        # Condición 2: Dispositivo REALMENTE lejos (confianza >80%)
        if proximity_result['is_away'] and proximity_result['confidence'] > 0.80:
            conditions_met.append("✓ Dispositivo REALMENTE lejos (>80%)")
        
        # Condición 3: NO es el usuario (confianza >80%)
        if not identity_result['is_user'] and identity_result['confidence'] > 0.80:
            conditions_met.append("✓ NO es el usuario (>80%)")
        
        print("\n" + "─"*80)
        
        # DECISIÓN: Requiere TODAS las condiciones
        if len(conditions_met) == 3:
            print("\n✓ TODAS LAS CONDICIONES CONFIRMADAS")
            print("Razones:")
            for c in conditions_met:
                print(f"  {c}")
            
            print("\n🚨 ACCIÓN: CAPTURAR FOTO + EMITIR ALARMA")
            print("⚠️ NO CONTACTAR POLICÍA (evitar falsas alarmas)")
            print("⚠️ ALERTAR A FAMILIA para que ellos contacten si es necesario")
            
            self.threat_confidence = 0.95
            self.alert_level = "CRÍTICA"
            self.requires_police = False  # ← NO contatar policía automáticamente
            
            return {
                "activate_alarm": True,
                "alert_family": True,
                "contact_police": False,  # ← IMPORTANTE: NO automático
                "reason": "Evidencia clara de robo/amenaza",
                "threat_confidence": 0.95,
                "action": "FOTO + ALARMA + ALERTA FAMILIA"
            }
        
        # Condición parcial: 2 de 3
        elif len(conditions_met) >= 2:
            print("\n⚠️ 2 DE 3 CONDICIONES CONFIRMADAS")
            print("Razones:")
            for c in conditions_met:
                print(f"  {c}")
            
            print("\n🟡 ACCIÓN: ALERTA SILENCIOSA A FAMILIA")
            print("⚠️ Sin alarma (evitar falsa alarma)")
            print("⚠️ Familia puede evaluar y contactar policía si es necesario")
            
            self.threat_confidence = 0.70
            self.alert_level = "MEDIA"
            self.requires_police = False
            
            return {
                "activate_alarm": False,
                "alert_family": True,
                "contact_police": False,
                "reason": "Posible amenaza (confianza media)",
                "threat_confidence": 0.70,
                "action": "ALERTA SILENCIOSA A FAMILIA"
            }
        
        # Menos de 2 condiciones
        else:
            print("\n✓ INSUFICIENTE EVIDENCIA")
            print("Razón: No se cumplen suficientes condiciones de riesgo")
            
            print("\n✓ ACCIÓN: CONTINUAR MONITOREO")
            print("✓ Sin alarma, sin alertas")
            
            self.threat_confidence = 0.0
            self.alert_level = "NORMAL"
            self.requires_police = False
            
            return {
                "activate_alarm": False,
                "alert_family": False,
                "contact_police": False,
                "reason": "No hay evidencia clara de amenaza",
                "threat_confidence": 0.0,
                "action": "CONTINUAR MONITOREO"
            }

    @safe_method
    def get_status(self):
        """Retorna estado"""
        return {
            "alert_level": self.alert_level,
            "threat_confidence": self.threat_confidence,
            "requires_police": self.requires_police,
            "status": f"Amenaza: {self.alert_level} ({self.threat_confidence*100:.0f}%)"
        }