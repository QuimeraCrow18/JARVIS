 # ==========================================
# CRIMINAL BEHAVIOR PATTERNS
# Detecta patrones típicos de delincuentes
# modules/criminal_behavior_patterns.py
# ==========================================

from core.utils import safe_method

class CriminalBehaviorPatterns:
    def __init__(self):
        print("[CRIMINAL-PATTERNS] Analizador de patrones criminales iniciado.")
        
        self.patterns = {
            "secuestro_extorsion": {
                "keywords": ["familia", "secuestrada", "dinero", "teléfono", "no avises"],
                "score_weight": 15,
                "threat_level": "🚨 CRÍTICA"
            },
            "estafa_financiera": {
                "keywords": ["banco", "transferencia", "tarjeta", "urgente"],
                "score_weight": 10,
                "threat_level": "⚠️ ALTA"
            },
            "scam_impostacion": {
                "keywords": ["policía", "irs", "oficial", "verificar"],
                "score_weight": 8,
                "threat_level": "⚠️ ALTA"
            },
            "romance_scam": {
                "keywords": ["te amo", "dinero", "viaje", "emergencia", "cuidar"],
                "score_weight": 7,
                "threat_level": "🟡 MEDIA"
            },
            "tech_support_scam": {
                "keywords": ["virus", "computadora", "hackeo", "soporte", "acceso"],
                "score_weight": 6,
                "threat_level": "🟡 MEDIA"
            },
            "sextortion": {
                "keywords": ["video", "fotografía", "desnudo", "vergüenza", "publicar"],
                "score_weight": 15,
                "threat_level": "🚨 CRÍTICA"
            },
            "rapto_virtual": {
                "keywords": ["tenemos", "capturamos", "en nuestro poder", "retenido"],
                "score_weight": 18,
                "threat_level": "🚨 CRÍTICA"
            }
        }

    @safe_method
    def analyze_criminal_pattern(self, transcript):
        """
        Identifica qué patrón criminal se está usando
        """
        criminal_patterns = []
        highest_score = 0
        detected_pattern = None
        
        transcript_lower = transcript.lower()
        
        for pattern_name, pattern_data in self.patterns.items():
            pattern_score = 0
            matched_keywords = []
            
            for keyword in pattern_data["keywords"]:
                if keyword in transcript_lower:
                    pattern_score += pattern_data["score_weight"]
                    matched_keywords.append(keyword)
            
            if pattern_score > 0:
                criminal_patterns.append({
                    "pattern": pattern_name.upper(),
                    "score": pattern_score,
                    "threat_level": pattern_data["threat_level"],
                    "matched_keywords": matched_keywords
                })
                
                if pattern_score > highest_score:
                    highest_score = pattern_score
                    detected_pattern = pattern_name
        
        criminal_patterns.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "detected_patterns": criminal_patterns,
            "primary_pattern": detected_pattern.upper() if detected_pattern else "DESCONOCIDO",
            "crime_type": self._classify_crime(detected_pattern),
            "priority_action": self._action_for_crime(detected_pattern)
        }

    @safe_method
    def detect_organized_crime_indicators(self, transcript):
        """
        Detecta indicadores de crimen organizado vs estafador individual
        """
        organized_indicators = []
        score = 0
        
        organized_phrases = {
            "somos": 10,
            "nuestro grupo": 15,
            "nosotros control": 15,
            "la cartera": 20,
            "la mafia": 20,
            "los sicarios": 20,
            "orden desde": 15,
            "me reporto a": 15,
            "tenemos red": 12,
            "sabemos todo": 12,
        }
        
        transcript_lower = transcript.lower()
        
        for phrase, weight in organized_phrases.items():
            if phrase in transcript_lower:
                organized_indicators.append(f"🔴 {phrase}")
                score += weight
        
        score = min(score, 100)
        
        return {
            "organized_crime_score": score,
            "is_organized_crime": score >= 40,
            "indicators": organized_indicators,
            "threat_classification": "🚨 CRIMEN ORGANIZADO" if score >= 60 else "⚠️ POSIBLE GRUPO" if score >= 40 else "👤 ESTAFADOR INDIVIDUAL"
        }

    @safe_method
    def _classify_crime(self, pattern):
        """Clasifica tipo de delito"""
        crime_map = {
            "secuestro_extorsion": "🚨 SECUESTRO/EXTORSIÓN",
            "estafa_financiera": "💰 ESTAFA FINANCIERA",
            "scam_impostacion": "🎭 SUPLANTACIÓN DE IDENTIDAD",
            "romance_scam": "💔 ESTAFA ROMÁNTICA",
            "tech_support_scam": "💻 ESTAFA TÉCNICA",
            "sextortion": "🔞 SEXTORSIÓN",
            "rapto_virtual": "👤 RAPTO VIRTUAL",
        }
        
        return crime_map.get(pattern, "DELITO DESCONOCIDO")

    @safe_method
    def _action_for_crime(self, pattern):
        """Recomienda acción para tipo de delito"""
        action_map = {
            "secuestro_extorsion": "CONTACTAR POLICÍA INMEDIATAMENTE + ALERTAR FAMILIA",
            "estafa_financiera": "BLOQUEAR TRANSFERENCIAS + ALERTAR BANCO",
            "scam_impostacion": "COLGAR + REPORTAR + NO COMPARTIR DATOS",
            "romance_scam": "EDUCACIÓN + BLOQUEAR + REPORTAR",
            "tech_support_scam": "COLGAR + CAMBIAR CONTRASEÑAS + SCAN ANTIVIRUS",
            "sextortion": "NO PAGAR + BLOQUEAR + REPORTAR A PLATAFORMA",
            "rapto_virtual": "LLAMAR POLICÍA + VERIFICAR CON FAMILIA",
        }
        
        return action_map.get(pattern, "CONTACTAR AUTORIDADES")