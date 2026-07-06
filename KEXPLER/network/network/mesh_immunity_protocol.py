import logging
import hmac
import hashlib

logging.basicConfig(level=logging.INFO, format='[JOSAMICK-MESH-IMMUNITY] %(asctime)s - %(levelname)s - %(message)s')

class MeshImmunityProtocol:
    def __init__(self):
        # Llave maestra compartida entre tus dispositivos del búnker para firmar paquetes offline
        self.LLAVE_SECRETA_MESH = b"JOSAMICK_MESH_TRUST_KEY_2026"
        # Registro en memoria de nodos autorizados activos en la vecindad mesh
        self.nodos_blancos_activos = set()

    def generar_firma_nodo(self, dispositivo_id: str, timestamp: str) -> str:
        """Genera una firma criptográfica única usando HMAC-SHA256 para validar el dispositivo."""
        mensaje = f"{dispositivo_id}:{timestamp}".encode()
        return hmac.new(self.LLAVE_SECRETA_MESH, mensaje, hashlib.sha256).hexdigest()

    def evaluar_trafico_mesh(self, dispositivo_id: str, timestamp: str, firma_recibida: str, tipo_conexion: str) -> dict:
        """
        Analiza si el dispositivo que se está introduciendo por detrás de la red
        es un puente legítimo de nuestra malla o un atacante real.
        """
        # 1. Verificar autenticidad criptográfica de la firma del nodo
        firma_esperada = self.generar_firma_nodo(dispositivo_id, timestamp)

        if hmac.compare_digest(firma_esperada, firma_recibida):
            self.nodos_blancos_activos.add(dispositivo_id)
            logging.info(f"🟢 [INMUNIDAD ACTIVADA] Dispositivo confiable '{dispositivo_id}' cruzando en modo {tipo_conexion}. EXENTO DE BLOQUEO.")
            return {
                "permitir_acceso": True,
                "detectado_como_intruso": False,
                "motivo": "Firma de confianza válida. Tráfico Mesh legítimo en puente local."
            }

        # 2. Si no tiene firma y se mete por detrás de la red, es un hacker real
        if tipo_conexion in ["PUENTE_LOCAL", "AD_HOC", "DIRECT_WIFI"]:
            logging.warning(f"🚨 [ALERTA DE INTRUSIÓN] Intento de acceso no autorizado por detrás de la red desde: {dispositivo_id}!")
            return {
                "permitir_acceso": False,
                "detectado_como_intruso": True,
                "motivo": "Intruso detectado intentando saltar por la red Mesh sin credenciales."
            }

        return {"permitir_acceso": False, "detectado_como_intruso": True, "motivo": "Tráfico denegado por defecto."}


if __name__ == "__main__":
    print("[📡] PROTOCOLO DE EXENCIÓN DE FUEGO AMIGO EN GUARDIA...")
    protocolo = MeshImmunityProtocol()

    # Prueba 1: Simulamos tu Moto G60 cruzando datos de forma local sin internet
    firma_g60 = protocolo.generar_firma_nodo("MotoG60_Bunker", "1718733400")
    print(protocolo.evaluar_trafico_mesh("MotoG60_Bunker", "1718733400", firma_g60, "PUENTE_LOCAL"))
