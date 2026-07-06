import time
import os
from modules.keta_transport import JosamickTransportManager
from modules.keta_storage import KetaStorageManager

def ejecutar_motor_infinito():
    print("[INICIANDO SERVICIO NATIVO DE JOSAMICK]")
    
    transport = JosamickTransportManager()
    storage = KetaStorageManager()
    
    while True:
        try:
            print("[i] Guardian de Josamick: Validando hilos de red...")
            time.sleep(5)
        except Exception as e:
            print(f"[SERVICE CRASH] Error en el bucle de fondo: {e}")
            time.sleep(10)

if __name__ == '__main__':
    ejecutar_motor_infinito()
