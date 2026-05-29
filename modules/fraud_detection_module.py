# ==========================================
# FRAUD DETECTION MODULE
# modules/fraud_detection_module.py
# ==========================================

from modules.threat_analyzer import ThreatAnalyzer
from modules.secure_communication import SecureMessenger
from core.utils import safe_method
from datetime import datetime
import json

class FraudDetectionModule:
    def __init__(self, device_id=None):
        print("[FRAUD-DETECTION] Módulo de detección de fraude iniciado.")
        self.threat_analyzer = ThreatAnalyzer()
        self.secure_messenger = SecureMessenger(device_id)
        self.call_history = []
        self.blocked_numbers = set()
        self.trusted_contacts = {}

    @safe_method
    def initialize_security(self, password):
        """Inicializa el cifrado E2E del dispositivo"""
        self.secure_messenger.setup_encryption_key(password)
        print("[FRAUD-DETECTION] Sistema de seguridad inicializado.")
        return True

    @safe_method
    def add_family_member(self, name, device_id, phone_number):
        """Agrega un familiar de confianza para recibir alertas"""
        self.secure_messenger.add_trusted_contact(name, device_id, phone_number)
        self.trusted_contacts[device_id] = {
            "name": name,
            "phone": phone_number,
            "alerts_sent": 0
        }
        return True

    @safe_method
    def process_incoming_call(self, caller_phone, caller_name="Desconocido", is_voip=False, is_hidden=False):
        """Procesa una llamada entrante y analiza la amenaza"""
        caller_info = {
            "phone": caller_phone,
            "name": caller_name,
            "is_voip": is_voip,
            "is_hidden": is_hidden,
            "is_unknown": caller_name == "Desconocido",
            "repeated_calls": self._count_repeated_calls(caller_phone),
            "time_of_call": datetime.now().hour
        }
        
        if caller_phone in self.blocked_numbers:
            print(f"[FRAUD-DETECTION] ⛔ Número bloqueado: {caller_phone}")
            return {
                "action": "BLOCK",
                "reason": "Número en lista negra",
                "threat_score": 100
            }
        
        return {
            "status": "ANALYZING",
            "caller_info": caller_info,
            "awaiting_transcript": True
        }

    @safe_method
    def analyze_call_transcript(self, transcript, caller_phone, caller_name="Desconocido"):
        """Analiza la transcripción de una llamada"""
        caller_info = {
            "phone": caller_phone,
            "name": caller_name,
            "is_voip": False,
            "is_hidden": caller_phone == "Oculto",
            "is_unknown": caller_name == "Desconocido",
            "repeated_calls": self._count_repeated_calls(caller_phone),
            "time_of_call": datetime.now().hour
        }
        
        threat_analysis = self.threat_analyzer.combined_threat_analysis(transcript, caller_info)
        self._save_call_record(caller_phone, caller_name, transcript, threat_analysis)
        
        return threat_analysis

    @safe_method
    def trigger_alert_to_family(self, threat_data, caller_info):
        """Si la amenaza es detectada, envía alerta cifrada a todos los familiares"""
        if threat_data["overall_threat_score"] < 50:
            print("[FRAUD-DETECTION] Amenaza no significativa, sin alertas")
            return False
        
        alerts_sent = []
        threat_data["caller_info"] = caller_info
        
        for device_id in self.trusted_contacts.keys():
            try:
                encrypted_alert = self.secure_messenger.send_threat_alert(threat_data, device_id)
                confirmation = self.secure_messenger.send_confirmation_request(threat_data, device_id)
                
                alerts_sent.append({
                    "device_id": device_id,
                    "family_member": self.trusted_contacts[device_id]["name"],
                    "alert_status": "ENVIADA",
                    "timestamp": datetime.now().isoformat()
                })
                
                self.trusted_contacts[device_id]["alerts_sent"] += 1
                
            except Exception as e:
                print(f"[FRAUD-DETECTION] Error enviando alerta: {e}")
        
        print(f"[FRAUD-DETECTION] 🚨 ALERTA ENVIADA A {len(alerts_sent)} FAMILIARES")
        return {
            "alerts_sent": len(alerts_sent),
            "recipients": alerts_sent,
            "threat_score": threat_data["overall_threat_score"]
        }

    @safe_method
    def block_number(self, phone_number):
        """Bloquea un número después de confirmación"""
        self.blocked_numbers.add(phone_number)
        print(f"[FRAUD-DETECTION] ✓ Número bloqueado: {phone_number}")
        return True

    @safe_method
    def get_call_history(self, limit=10):
        """Retorna el historial de llamadas analizadas"""
        return self.call_history[-limit:]

    @safe_method
    def _count_repeated_calls(self, phone_number):
        """Cuenta cuántas veces ha llamado este número"""
        return sum(1 for call in self.call_history if call.get("caller_phone") == phone_number)

    @safe_method
    def _save_call_record(self, phone, name, transcript, analysis):
        """Guarda registro de la llamada en historial"""
        record = {
            "caller_phone": phone,
            "caller_name": name,
            "transcript": transcript[:200] if transcript else "Sin transcripción",
            "threat_score": analysis["overall_threat_score"],
            "risk_level": analysis["content_analysis"]["risk_level"],
            "timestamp": datetime.now().isoformat(),
            "action_taken": analysis["recommended_action"]
        }
        self.call_history.append(record)
        return True

    @safe_method
    def export_security_report(self):
        """Genera un reporte de seguridad"""
        return {
            "device_id": self.secure_messenger.device_id,
            "total_calls_analyzed": len(self.call_history),
            "suspicious_calls": sum(1 for call in self.call_history if call["threat_score"] >= 50),
            "blocked_numbers": list(self.blocked_numbers),
            "family_members": len(self.trusted_contacts),
            "alerts_sent": sum(c["alerts_sent"] for c in self.trusted_contacts.values()),
            "recent_threats": self.get_call_history(5)
        }