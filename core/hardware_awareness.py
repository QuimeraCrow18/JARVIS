"""Hardware Awareness: consciencia de hardware para JARVIS.
Detecta el entorno (PC, Android, TV, etc.) y ajusta el comportamiento."""

import os
import sys
import platform
import socket
import threading
from datetime import datetime
from enum import Enum
from typing import Optional


class HardwareProfile(Enum):
    FULL_MODE = "full"
    LIGHT_MODE = "light"
    OFFLINE_MODE = "offline"


class HardwareDetector:
    def __init__(self):
        self.profile: HardwareProfile = HardwareProfile.FULL_MODE
        self.system: str = platform.system().lower()
        self.machine: str = platform.machine().lower()
        self.processor: str = platform.processor()
        self.python_version: str = sys.version
        self._detect_environment()

    def _detect_environment(self):
        """Detecta el entorno y asigna el perfil por defecto."""
        is_android = "android" in self.system or "linux" in self.system and "ANDROID_ROOT" in os.environ
        is_webos = "webos" in self.system or "webos" in platform.platform().lower()
        is_linux = self.system == "linux" and not is_android and not is_webos
        is_windows = self.system == "windows"
        is_darwin = self.system == "darwin"
        is_smarttv = any(kw in platform.platform().lower() for kw in ["tizen", "webos", "smarttv"])

        # Lite environments
        limited_memory = self._get_available_memory() < 1024 if self._get_available_memory() else False
        is_limited = is_android or is_smarttv or limited_memory

        if is_limited:
            self.profile = HardwareProfile.LIGHT_MODE
        elif not self._has_network():
            self.profile = HardwareProfile.OFFLINE_MODE
        else:
            self.profile = HardwareProfile.FULL_MODE

    def _get_available_memory(self) -> Optional[float]:
        """Retorna memoria disponible en MB."""
        try:
            if self.system == "linux":
                with open("/proc/meminfo") as f:
                    for line in f:
                        if "MemAvailable" in line:
                            return int(line.split()[1]) / 1024
            elif self.system == "windows":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                mem = ctypes.c_longlong()
                kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
                return mem.value / (1024 ** 3)
            elif self.system == "darwin":
                import subprocess
                result = subprocess.run(["sysctl", "hw.memsize"], capture_output=True, text=True)
                return int(result.stdout.split()[1]) / (1024 ** 3)
        except Exception:
            pass
        return None

    def _has_network(self, timeout=2) -> bool:
        """Verifica conectividad de red."""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            return True
        except OSError:
            return False

    @property
    def has_internet(self) -> bool:
        return self._has_network()

    def run(self) -> dict:
        """Ejecuta la detección y retorna el reporte completo."""
        report = {
            "profile": self.profile.value,
            "system": self.system,
            "machine": self.machine,
            "processor": self.processor,
            "python": self.python_version,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "memory_mb": self._get_available_memory(),
            "network": self._has_network(),
        }
        print(f"[HARDWARE] Perfil detectado: {self.profile.value.upper()} ({self.system})")
        return report

    def get_boot_flags(self) -> dict:
        """Retorna flags de arranque según el perfil."""
        flags = {
            "auto_evolution": True,
            "load_vision": True,
            "load_voice": True,
            "load_network_modules": True,
            "background_tasks": True,
        }
        if self.profile == HardwareProfile.LIGHT_MODE:
            flags.update({
                "auto_evolution": False,
                "load_vision": False,
                "background_tasks": False,
            })
        elif self.profile == HardwareProfile.OFFLINE_MODE:
            flags.update({
                "load_network_modules": False,
                "auto_evolution": False,
            })
        return flags


class NetworkInterceptor:
    """Intercepta fallos de red y fuerza OFFLINE_MODE sin detener el sistema."""

    def __init__(self, detector: HardwareDetector):
        self.detector = detector
        self._lock = threading.Lock()

    def check_and_switch(self, error: str) -> bool:
        """Detecta timeout de red y cambia a OFFLINE_MODE."""
        if not error:
            return False
        timeout_keywords = ["timeout", "network", "connection refused", "no route to host",
                           "timed out", "econnrefused", "enotreach", "ehostunreach"]
        should_switch = any(kw in error.lower() for kw in timeout_keywords)
        if should_switch:
            with self._lock:
                if self.detector.profile != HardwareProfile.OFFLINE_MODE:
                    old = self.detector.profile
                    self.detector.profile = HardwareProfile.OFFLINE_MODE
                    print(f"[NETWORK] Timeout detectado — cambiando de {old.value} a OFFLINE_MODE")
            return True
        return False


def intercept_network_timeout(func):
    """Decorador: envuelve funciones de red para atrapar timeouts."""
    interceptor = None

    def wrapper(*args, **kwargs):
        nonlocal interceptor
        if interceptor is None:
            detector = HardwareDetector()
            interceptor = NetworkInterceptor(detector)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            interceptor.check_and_switch(str(e))
            raise
    return wrapper


if __name__ == "__main__":
    detector = HardwareDetector()
    report = detector.run()
    print(f"[OK] HardwareDetector inicializado. Perfil: {report['profile']}")
