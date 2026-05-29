# ==========================================
# IDENTITY SPOOFING DETECTOR
# Detecta suplantación de identidad
# modules/identity_spoofing_detector.py
# ==========================================

from core.utils import safe_method
import re
from datetime import datetime

class IdentitySpoofingDetector:
    def __init__(self):
        print("[SPOOFING-DETECTOR] Detector de suplantación iniciado.")
        
        self.legitimate_banks = {
            "Bank of America": ["1-800-432-1000", "1-800-769-2511"],
            "Chase": ["1-800-935-9935", "1-888-935-1010"],
            "Wells Fargo": ["1-800-869-3557"],
            "Citibank": ["1-800-950-5114"],
            "BBVA": ["+34-902-224-466"],
            "Santander": ["+34-902-242-424"],
            "CaixaBank": ["+34-902-012-012"],
        }
        
        self.legitimate_government = {
            "IRS": ["1-800-829-1040"],
            "Social Security": ["1-800-772-1213"],
            "Medicare": ["1-800-633-4227"],
        }

    @safe_method
    def analyze_caller_legitimacy(self, caller_phone, caller_name, claimed_institution):
        """
        Analiza si el número telefónico coincide con la institución reclamada
        """
        spoofing_score = 0
        red_flags = []
        
        if claimed_institution:
            claimed_lower = claimed_institution.lower()
            
            is_legitimate = self._check_legitimate_number(caller_phone, claimed_institution)
            
            if not is_legitimate:
                spoofing_score += 40
                red_flags.append(f"❌ Número {caller_phone} NO es oficial de {claimed_institution}")
            
            if self._is_spoofed_pattern(caller_phone):
                spoofing_score += 30
                red_flags.append("🔴 Patrón de número SOSPECHOSO (spoofing típico)")
        
        if caller_phone == "Oculto" or "Unknown" in caller_phone:
            spoofing_score += 25
            red_flags.append("🔴 Número OCULTO o DESCONOCIDO")
        
        if self._is_voip_number(caller_phone):
            spoofing_score += 15
            red_flags.append("📱 Llamada VoIP (común en estafas)")
        
        spoofing_score = min(spoofing_score, 100)
        
        return {
            "spoofing_score": spoofing_score,
            "is_likely_spoofed": spoofing_score >= 50,
            "red_flags": red_flags,
            "confidence": self._calculate_spoofing_confidence(spoofing_score),
            "recommendation": self._spoofing_recommendation(spoofing_score)
        }

    @safe_method
    def detect_impersonation(self, transcript, claimed_identity):
        """
        Detecta si alguien está fingiendo ser una entidad específica
        """
        impersonation_score = 0
        impersonation_indicators = []
        
        transcript_lower = transcript.lower()
        
        impersonation_phrases = {
            "soy del banco": 8,
            "habla seguridad": 10,
            "habla la policía": 12,
            "irs aquí": 10,
            "seguro social": 8,
            "verificando tu cuenta": 9,
            "confirmando datos": 8,
            "sistema de seguridad": 10,
            "departamento de fraude": 9,
            "oficial aquí": 10,
            "investigador": 8,
            "agente especial": 10,
            "tengo acceso a tus registros": 12,
        }
        
        for phrase, weight in impersonation_phrases.items():
            if phrase in transcript_lower:
                impersonation_score += weight
                impersonation_indicators.append(f"'{phrase}' detectado")
        
        if claimed_identity and claimed_identity.lower() not in transcript_lower:
            impersonation_score += 10
            impersonation_indicators.append("Identidad reclamada NO mencionada en llamada")
        
        impersonation_score = min(impersonation_score, 100)
        
        return {
            "impersonation_score": impersonation_score,
            "is_impersonating": impersonation_score >= 45,
            "indicators": impersonation_indicators,
            "likely_impersonating_as": self._detect_impersonated_entity(transcript)
        }

    @safe_method
    def _check_legitimate_number(self, phone, institution):
        """Verifica si es un número legítimo conocido"""
        all_legit = {**self.legitimate_banks, **self.legitimate_government}
        
        if institution in all_legit:
            return phone in all_legit[institution]
        
        return False

    @safe_method
    def _is_spoofed_pattern(self, phone_number):
        """Detecta patrones típicos de spoofing"""
        spoofed_patterns = [
            r"1-800-",
            r"555-",
            r"666-",
        ]
        
        for pattern in spoofed_patterns:
            if re.search(pattern, phone_number):
                return True
        
        return False

    @safe_method
    def _is_voip_number(self, phone_number):
        """Detecta si es número VoIP"""
        voip_patterns = [
            "Google Voice",
            "Skype",
            "WhatsApp",
            "Telegram",
            "+1-201-",
            "+1-202-",
        ]
        
        for pattern in voip_patterns:
            if pattern in phone_number:
                return True
        
        return False

    @safe_method
    def _calculate_spoofing_confidence(self, score):
        """Calcula confianza de spoofing"""
        if score >= 80:
            return 0.98
        elif score >= 60:
            return 0.85
        elif score >= 40:
            return 0.65
        else:
            return 0.40

    @safe_method
    def _spoofing_recommendation(self, score):
        """Recomienda acción según score"""
        if score >= 80:
            return "🚫 BLOQUEAR INMEDIATAMENTE - DEFINITIVAMENTE SPOOFING"
        elif score >= 60:
            return "⚠️ PROBABLE SPOOFING - NO COMPARTIR DATOS"
        elif score >= 40:
            return "🟡 SOSPECHOSO - VERIFICAR CON INSTITUCIÓN DIRECTAMENTE"
        else:
            return "✓ PROBABLEMENTE LEGÍTIMO"

    @safe_method
    def _detect_impersonated_entity(self, transcript):
        """Detecta quién está intentando suplantar"""
        entities = {
            "banco": ["bank", "cuenta", "tarjeta", "transferencia", "saldo"],
            "policía": ["policía", "arresto", "delito", "investigación", "legal"],
            "irs": ["impuestos", "irs", "reembolso", "multa", "auditoría"],
            "seguro social": ["social security", "ssn", "beneficios", "número"],
            "amazon": ["amazon", "orden", "paquete", "reembolso", "cuenta"],
            "apple": ["apple", "icloud", "id", "cuenta", "suscripción"],
            "microsoft": ["microsoft", "windows", "virus", "soporte", "acceso"],
        }
        
        transcript_lower = transcript.lower()
        detected = []
        
        for entity, keywords in entities.items():
            if any(keyword in transcript_lower for keyword in keywords):
                detected.append(entity.upper())
        
        return detected if detected else ["DESCONOCIDA"]