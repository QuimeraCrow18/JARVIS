# ==========================================
# SECURE COMMUNICATION MODULE
# Cifrado E2E de dispositivo a dispositivo
# modules/secure_communication.py
# ==========================================

import os
import json
import base64
from core.utils import safe_method

class SecureMessenger:
    def __init__(self, device_id=None):
        self._crypto_available = False
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
            from cryptography.hazmat.backends import default_backend
            self.Fernet = Fernet
            self.hashes = hashes
            self.PBKDF2 = PBKDF2
            self.default_backend = default_backend
            self._crypto_available = True
        except Exception as e:
            print(f"[SECURE-COMM] Criptografía no disponible: {e}")
        print("[SECURE-COMM] Sistema de comunicación segura iniciado.")
        self.device_id = device_id or self._generate_device_id()
        self.cipher = None
        self.contacts = {}  # Almacena contactos de confianza
        
    @safe_method
    def _generate_device_id(self):
        """Genera un ID único del dispositivo"""
        return base64.urlsafe_b64encode(os.urandom(16)).decode()
    
    @safe_method
    def setup_encryption_key(self, password):
        if not self._crypto_available:
            print("[SECURE-COMM] Criptografía no disponible")
            return False
        salt = b'jarvis_threat_alert_2026'
        kdf = self.PBKDF2(
            algorithm=self.hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = self.Fernet(key)
        print("[SECURE-COMM] Clave de cifrado configurada.")
        return True

    @safe_method
    def encrypt_message(self, message, recipient_key=None):
        if not self._crypto_available or not self.cipher:
            print("[SECURE-COMM] Error: Cifrado no disponible")
            return None
        message_json = json.dumps(message)
        encrypted = self.cipher.encrypt(message_json.encode())
        
        return {
            "from_device": self.device_id,
            "to_device": recipient_key,
            "encrypted_payload": encrypted.decode(),
            "timestamp": self._get_timestamp()
        }

    @safe_method
    def decrypt_message(self, encrypted_data):
        if not self._crypto_available or not self.cipher:
            print("[SECURE-COMM] Error: Cifrado no disponible")
            return None
        
        try:
            decrypted = self.cipher.decrypt(encrypted_data["encrypted_payload"].encode())
            message = json.loads(decrypted.decode())
            return message
        except Exception as e:
            print(f"[SECURE-COMM] Error descifrando: {e}")
            return None

    @safe_method
    def add_trusted_contact(self, contact_name, device_id, phone_number):
        """
        Añade un contacto de confianza (familiar)
        """
        self.contacts[device_id] = {
            "name": contact_name,
            "device_id": device_id,
            "phone_number": phone_number,
            "added_at": self._get_timestamp()
        }
        print(f"[SECURE-COMM] Contacto '{contact_name}' añadido.")
        return True

    @safe_method
    def send_threat_alert(self, threat_data, recipient_device_id):
        """
        Envía una alerta de amenaza cifrada a otro dispositivo
        """
        if recipient_device_id not in self.contacts:
            print(f"[SECURE-COMM] Error: {recipient_device_id} no es contacto de confianza")
            return False
        
        alert_message = {
            "type": "THREAT_ALERT",
            "threat_level": threat_data["overall_threat_score"],
            "threat_type": threat_data["content_analysis"].get("risk_level"),
            "recommended_action": threat_data["recommended_action"],
            "timestamp": self._get_timestamp(),
            "caller_info": threat_data.get("caller_info"),
            "keywords_detected": [kw[0] for kw in threat_data["content_analysis"].get("detected_keywords", [])]
        }
        
        encrypted_alert = self.encrypt_message(alert_message, recipient_device_id)
        
        print(f"[SECURE-COMM] Alerta enviada cifrada a {self.contacts[recipient_device_id]['name']}")
        return encrypted_alert

    @safe_method
    def send_confirmation_request(self, threat_data, recipient_device_id):
        """
        Solicita confirmación del familiar sobre una amenaza potencial
        """
        confirmation_request = {
            "type": "CONFIRMATION_REQUEST",
            "threat_score": threat_data["overall_threat_score"],
            "threat_details": threat_data["content_analysis"].get("detected_keywords"),
            "caller_info": threat_data.get("caller_info"),
            "timestamp": self._get_timestamp(),
            "requires_response": True
        }
        
        encrypted_request = self.encrypt_message(confirmation_request, recipient_device_id)
        print(f"[SECURE-COMM] Solicitud de confirmación enviada a {self.contacts[recipient_device_id]['name']}")
        return encrypted_request

    @safe_method
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()