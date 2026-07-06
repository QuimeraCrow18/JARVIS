import sys
import platform as _stdlib_platform
import os


class PlatformDetector:

    def __init__(self):
        self._system = _stdlib_platform.system().lower()
        self._machine = _stdlib_platform.machine().lower()
        self._python_impl = _stdlib_platform.python_implementation()
        self._android_env = os.environ.get("ANDROID_ARGUMENT") or os.environ.get("ANDROID_ROOT")

    @property
    def is_windows(self):
        return self._system == "windows"

    @property
    def is_linux(self):
        return self._system == "linux" and not self.is_android

    @property
    def is_macos(self):
        return self._system == "darwin"

    @property
    def is_android(self):
        return bool(self._android_env) or "android" in self._python_impl.lower()

    @property
    def is_termux(self):
        return self.is_android and "com.termux" in os.environ.get("PREFIX", "")

    @property
    def is_raspberry_pi(self):
        if not self.is_linux:
            return False
        try:
            with open("/proc/cpuinfo") as f:
                return "BCM" in f.read()
        except OSError:
            return False

    @property
    def is_mobile(self):
        return self.is_android

    @property
    def is_desktop(self):
        return self.is_windows or self.is_linux or self.is_macos

    @property
    def has_display(self):
        if self.is_windows:
            return True
        if self.is_macos:
            return True
        if self.is_linux:
            return os.environ.get("DISPLAY") is not None
        return False

    @property
    def name(self):
        if self.is_windows:
            return "windows"
        if self.is_macos:
            return "macos"
        if self.is_android:
            return "android"
        if self.is_raspberry_pi:
            return "raspberry-pi"
        if self.is_linux:
            return "linux"
        return self._system

    @property
    def friendly_name(self):
        names = {
            "windows": "Windows",
            "macos": "macOS",
            "android": "Android",
            "raspberry-pi": "Raspberry Pi",
            "linux": "Linux",
        }
        return names.get(self.name, self._system.capitalize())

    def get_info(self):
        return {
            "platform": self.name,
            "friendly_name": self.friendly_name,
            "system": self._system,
            "machine": self._machine,
            "python": sys.version,
            "is_desktop": self.is_desktop,
            "is_mobile": self.is_mobile,
            "has_display": self.has_display,
        }

    def get_available_features(self):
        features = ["voice", "learning", "face_recognition", "web_remote"]

        if self.is_desktop:
            features.extend(["automation", "system_monitor", "gui", "file_search"])
            if self.has_display:
                features.extend(["media", "enhance"])

        if self.is_android:
            features.extend(["sms", "camera", "gps", "sensors"])

        if self.is_raspberry_pi:
            features.extend(["gpio", "sensors"])

        return features
