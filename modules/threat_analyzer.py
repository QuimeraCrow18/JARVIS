# ==========================================
# THREAT ANALYZER MODULE
# modules/threat_analyzer.py
# ==========================================

from core.utils import safe_method

class ThreatAnalyzer:
    def __init__(self):
        print("[THREAT-ANALYZER] Analizador de amenazas iniciado.")
        
        # Palabras clave comunes en estafas
        self.fraud_keywords = {
            "urgente": 5,
            "confirmar datos": 10,
            "número de tarjeta": 15,
            "contraseña": 12,
            "dinero": 8,
            "transferencia": 10,
            "banco": 7,
            "IRS": 12,
            "impuestos": 9,
            "multa": 10,
            "ganaste": 8,
            "premio": 9,
            "herencia": 11,
            "virus": 10,
            "hackeo": 10,
            "cuenta bloqueada": 12,
            "verificar identidad": 11,
            "código de seguridad": 13,
            "información personal": 14,
            "peligro": 8,
            "fraude": 15,
            "estafa": 15,
            "cuidado": 6,
            "llama ahora": 8,
            "no cuelgues": 10,
            "sólo hoy": 7,
            "oferta limitada": 8,
        }
        
        # Patrones de números sospechosos
        self.suspicious_patterns = {
            "VoIP": 3,
            "número oculto": 5,
            "desconocido": 2,
        }

    @safe_method
    def analyze_call_content(self, transcript):
        """
        Analiza el contenido de una llamada/transcripción
        y retorna un score de amenaza (0-100)
        """
        if not transcript:
            return 0
        
        transcript_lower = transcript.lower()
        threat_score = 0
        detected_keywords = []
        
        # Busca palabras clave de fraude
        for keyword, weight in self.fraud_keywords.items():
            if keyword in transcript_lower:
                threat_score += weight
                detected_keywords.append((keyword, weight))
        
        # Normaliza el score a 0-100
        threat_score = min(threat_score, 100)
        
        return {
            "threat_score": threat_score,
            "detected_keywords": detected_keywords,
            "is_suspicious": threat_score >= 40,
            "risk_level": self._get_risk_level(threat_score)
        }

    @safe_method
    def analyze_caller_pattern(self, caller_info):
        """
        Analiza patrones del llamante
        (número oculto, VoIP, histórico sospechoso, etc.)
        """
        pattern_score = 0
        suspicious_indicators = []
        
        if caller_info.get("is_hidden"):
            pattern_score += 5
            suspicious_indicators.append("Número oculto")
        
        if caller_info.get("is_voip"):
            pattern_score += 3
            suspicious_indicators.append("Llamada VoIP")
        
        if caller_info.get("is_unknown"):
            pattern_score += 2
            suspicious_indicators.append("Número desconocido")
        
        if caller_info.get("repeated_calls") > 3:
            pattern_score += 4
            suspicious_indicators.append(f"Múltiples llamadas ({caller_info['repeated_calls']})")
        
        if caller_info.get("time_of_call") in [0, 1, 2, 3, 4]:  # Madrugada
            pattern_score += 3
            suspicious_indicators.append("Llamada a hora sospechosa")
        
        pattern_score = min(pattern_score, 100)
        
        return {
            "pattern_score": pattern_score,
            "suspicious_indicators": suspicious_indicators,
            "is_risky": pattern_score >= 25
        }

    @safe_method
    def combined_threat_analysis(self, transcript, caller_info):
        """
        Análisis combinado: contenido + patrón del llamante
        """
        content_analysis = self.analyze_call_content(transcript)
        pattern_analysis = self.analyze_caller_pattern(caller_info)
        
        combined_score = (content_analysis["threat_score"] * 0.6) + (pattern_analysis["pattern_score"] * 0.4)
        combined_score = min(combined_score, 100)
        
        return {
            "overall_threat_score": combined_score,
            "content_analysis": content_analysis,
            "pattern_analysis": pattern_analysis,
            "is_threat": combined_score >= 50,
            "recommended_action": self._recommend_action(combined_score),
            "confidence": self._calculate_confidence(combined_score)
        }

    @safe_method
    def _get_risk_level(self, score):
        if score >= 80:
            return "CRÍTICO"
        elif score >= 60:
            return "ALTO"
        elif score >= 40:
            return "MEDIO"
        elif score >= 20:
            return "BAJO"
        else:
            return "SEGURO"

    @safe_method
    def _recommend_action(self, score):
        if score >= 80:
            return "BLOQUEAR INMEDIATAMENTE Y REPORTAR"
        elif score >= 60:
            return "NO COMPARTIR DATOS PERSONALES - COLGAR"
        elif score >= 40:
            return "VERIFICAR IDENTIDAD DEL LLAMANTE"
        elif score >= 20:
            return "PROCEDER CON CAUTELA"
        else:
            return "SEGURO - CONTINUAR"

    @safe_method
    def _calculate_confidence(self, score):
        # Qué tan seguro estamos de la amenaza
        if score >= 70:
            return 0.95  # 95% de confianza
        elif score >= 50:
            return 0.80
        elif score >= 30:
            return 0.60
        else:
            return 0.40