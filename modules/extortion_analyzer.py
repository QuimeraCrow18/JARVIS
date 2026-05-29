# ==========================================
# EXTORTION ANALYZER
# Detecta extorsión, chantaje, amenazas
# modules/extortion_analyzer.py
# ==========================================

from core.utils import safe_method

class ExtortionAnalyzer:
    def __init__(self):
        print("[EXTORTION-ANALYZER] Analizador de extorsión iniciado.")

    @safe_method
    def analyze_direct_threats(self, transcript):
        """
        Detecta amenazas DIRECTAS contra el usuario o familia
        """
        threat_score = 0
        threats_detected = []
        
        violence_threats = {
            "te voy a matar": 100,
            "vamos a matarte": 100,
            "le voy a hacer daño": 100,
            "te voy a golpear": 95,
            "acuérdate del nombre": 80,
            "sabemos dónde vives": 90,
            "tengo tu dirección": 90,
            "conozco tu familia": 85,
            "sabemos dónde trabaja": 85,
            "te vamos a encontrar": 85,
            "no te preocupes, iremos": 80,
            "te van a desaparecer": 100,
        }
        
        family_threats = {
            "tenemos a tu madre": 100,
            "capturamos a tu familia": 100,
            "tenemos a tu hija": 100,
            "tenemos a tu hijo": 100,
            "tu abuela": 95,
            "tu hermano": 95,
            "tus padres están aquí": 100,
            "la familia va a pagar": 100,
            "si no pagas les pasará algo": 100,
        }
        
        legal_threats = {
            "vamos a tu casa": 80,
            "mandamos policía": 70,
            "orden de arresto": 75,
            "demanda judicial": 60,
            "deuda con el gobierno": 60,
        }
        
        transcript_lower = transcript.lower()
        
        for threat, weight in violence_threats.items():
            if threat in transcript_lower:
                threat_score += weight
                threats_detected.append(("VIOLENCIA", threat, weight))
        
        for threat, weight in family_threats.items():
            if threat in transcript_lower:
                threat_score += weight
                threats_detected.append(("AMENAZA A FAMILIA", threat, weight))
        
        for threat, weight in legal_threats.items():
            if threat in transcript_lower:
                threat_score += weight
                threats_detected.append(("AMENAZA LEGAL", threat, weight))
        
        threat_score = min(threat_score, 100)
        
        return {
            "threat_score": threat_score,
            "has_direct_threats": threat_score >= 50,
            "threats_detected": threats_detected,
            "threat_type": self._classify_threat_type(threats_detected),
            "is_life_threatening": threat_score >= 75
        }

    @safe_method
    def analyze_extortion_demand(self, transcript):
        """
        Detecta demandas de dinero/datos bajo coacción
        """
        extortion_score = 0
        extortion_indicators = []
        
        money_demands = {
            "paga ahora": 20,
            "transferencia inmediata": 25,
            "dinero urgente": 20,
            "pago de multa": 25,
            "deuda con": 15,
            "pagos atrasados": 15,
            "tarjeta de crédito": 20,
            "gift card": 30,
            "bitcoin": 30,
            "western union": 30,
            "moneygram": 30,
            "criptomoneda": 25,
            "números de cuenta": 25,
            "números de seguridad": 25,
        }
        
        threat_context = {
            "o si no": 15,
            "si no pagas": 20,
            "si no haces": 20,
            "sino": 10,
            "o te": 15,
            "o vamos": 15,
        }
        
        transcript_lower = transcript.lower()
        
        for demand, weight in money_demands.items():
            if demand in transcript_lower:
                extortion_score += weight
                extortion_indicators.append(f"💰 Demanda: '{demand}'")
        
        for context, weight in threat_context.items():
            if context in transcript_lower:
                extortion_score += weight
                extortion_indicators.append(f"⚠️ Contexto de amenaza: '{context}'")
        
        extortion_score = min(extortion_score, 100)
        
        return {
            "extortion_score": extortion_score,
            "is_extortion": extortion_score >= 40,
            "indicators": extortion_indicators,
            "urgency_level": self._urgency_level(extortion_score)
        }

    @safe_method
    def analyze_psychological_manipulation(self, transcript):
        """
        Detecta técnicas de manipulación psicológica
        """
        manipulation_score = 0
        manipulation_tactics = []
        
        urgency_tactics = {
            "urgente": 10,
            "ahora mismo": 10,
            "inmediatamente": 10,
            "no esperes": 10,
            "rápido": 8,
            "antes de": 10,
            "límite de tiempo": 12,
            "hoy solamente": 10,
        }
        
        isolation_tactics = {
            "no digas nada": 15,
            "es confidencial": 12,
            "no le cuentes a nadie": 15,
            "secreto entre nosotros": 15,
            "no avises a": 15,
            "si le dices": 15,
        }
        
        trust_building = {
            "confía en mí": 10,
            "yo te ayudo": 8,
            "soy tu amigo": 12,
            "entiendo tu situación": 8,
            "te creo": 8,
        }
        
        authority_tactics = {
            "tengo poder": 10,
            "yo decido": 10,
            "no tienes opción": 12,
            "obedece": 15,
            "no preguntes": 12,
        }
        
        transcript_lower = transcript.lower()
        
        for tactic, weight in urgency_tactics.items():
            if tactic in transcript_lower:
                manipulation_score += weight
                manipulation_tactics.append(f"⏰ Crear urgencia: '{tactic}'")
        
        for tactic, weight in isolation_tactics.items():
            if tactic in transcript_lower:
                manipulation_score += weight
                manipulation_tactics.append(f"🔐 Aislamiento: '{tactic}'")
        
        for tactic, weight in trust_building.items():
            if tactic in transcript_lower:
                manipulation_score += weight
                manipulation_tactics.append(f"🤝 Ganar confianza: '{tactic}'")
        
        for tactic, weight in authority_tactics.items():
            if tactic in transcript_lower:
                manipulation_score += weight
                manipulation_tactics.append(f"👑 Afirmar autoridad: '{tactic}'")
        
        manipulation_score = min(manipulation_score, 100)
        
        return {
            "manipulation_score": manipulation_score,
            "is_manipulative": manipulation_score >= 35,
            "tactics_detected": manipulation_tactics,
            "psychological_risk": "ALTA" if manipulation_score >= 60 else "MEDIA" if manipulation_score >= 35 else "BAJA"
        }

    @safe_method
    def _classify_threat_type(self, threats_detected):
        """Clasifica el tipo de amenaza"""
        if any(t[0] == "AMENAZA A FAMILIA" for t in threats_detected):
            return "🚨 AMENAZA A FAMILIA - CRÍTICO"
        elif any(t[0] == "VIOLENCIA" for t in threats_detected):
            return "🚨 AMENAZA DE VIOLENCIA - CRÍTICO"
        elif any(t[0] == "AMENAZA LEGAL" for t in threats_detected):
            return "⚠️ AMENAZA LEGAL FALSA"
        else:
            return "DESCONOCIDO"

    @safe_method
    def _urgency_level(self, score):
        """Clasifica nivel de urgencia"""
        if score >= 70:
            return "🚨 URGENCIA CRÍTICA"
        elif score >= 50:
            return "⚠️ URGENCIA ALTA"
        elif score >= 30:
            return "🟡 MODERADO"
        else:
            return "ℹ️ BAJO"