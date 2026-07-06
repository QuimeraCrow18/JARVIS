import os
import hmac
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class OceanicShield:
    def __init__(self, clave=None):
        raw = clave or os.urandom(32)
        if isinstance(raw, str):
            self._clave = hashlib.sha256(raw.encode()).digest()
        else:
            self._clave = hashlib.sha256(raw).digest()
        self._clave_firma = hashlib.sha256(self._clave).digest()
        self.aes = AESGCM(self._clave)

    def encriptar(self, datos):
        if isinstance(datos, str): datos = datos.encode()
        nonce = os.urandom(12)
        return base64.b64encode(nonce + self.aes.encrypt(nonce, datos, None)).decode()

    def desencriptar(self, d):
        try:
            raw = base64.b64decode(d.encode())
            return self.aes.decrypt(raw[:12], raw[12:], None).decode()
        except: return None

    def firmar_paquete(self, datos):
        if isinstance(datos, str): datos = datos.encode()
        return hmac.new(self._clave_firma, datos, hashlib.sha256).hexdigest()

    def verificar_firma(self, datos, firma):
        if isinstance(datos, str): datos = datos.encode()
        return hmac.compare_digest(self.firmar_paquete(datos), firma)
