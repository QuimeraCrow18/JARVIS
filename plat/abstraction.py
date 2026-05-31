from plat.detector import PlatformDetector


class PlatformNotSupportedError(Exception):
    pass


detector = PlatformDetector()


class AutomationBackend:

    def open_app(self, app_name):
        raise NotImplementedError

    def open_website(self, url):
        raise NotImplementedError

    def shutdown(self):
        raise NotImplementedError

    def restart(self):
        raise NotImplementedError

    def lock(self):
        raise NotImplementedError

    @staticmethod
    def get_backend():
        if detector.is_windows:
            return _WindowsAutomation()
        if detector.is_linux:
            return _LinuxAutomation()
        if detector.is_macos:
            return _MacAutomation()
        return _FallbackAutomation()


class _WindowsAutomation(AutomationBackend):

    def open_app(self, app_name):
        import subprocess
        subprocess.Popen(["start", app_name], shell=True)

    def open_website(self, url):
        import webbrowser
        webbrowser.open(url)

    def shutdown(self):
        import os
        os.system("shutdown /s /t 5")

    def restart(self):
        import os
        os.system("shutdown /r /t 5")

    def lock(self):
        import os
        os.system("rundll32.exe user32.dll,LockWorkStation")


class _LinuxAutomation(AutomationBackend):

    def open_app(self, app_name):
        import subprocess
        subprocess.Popen(["xdg-open", app_name])

    def open_website(self, url):
        import webbrowser
        webbrowser.open(url)

    def shutdown(self):
        import os
        os.system("shutdown -h now")

    def restart(self):
        import os
        os.system("shutdown -r now")

    def lock(self):
        import os
        os.system("gnome-screensaver-command -l 2>/dev/null || loginctl lock-session")


class _MacAutomation(AutomationBackend):

    def open_app(self, app_name):
        import subprocess
        subprocess.Popen(["open", "-a", app_name])

    def open_website(self, url):
        import webbrowser
        webbrowser.open(url)

    def shutdown(self):
        import os
        os.system("osascript -e 'tell app \"System Events\" to shut down'")

    def restart(self):
        import os
        os.system("osascript -e 'tell app \"System Events\" to restart'")

    def lock(self):
        import os
        os.system("pmset displaysleepnow")


class _FallbackAutomation(AutomationBackend):

    def open_app(self, app_name):
        print(f"[AUTO] No se puede abrir '{app_name}' en {detector.friendly_name}")

    def open_website(self, url):
        import webbrowser
        webbrowser.open(url)

    def shutdown(self):
        print(f"[AUTO] Apagado no soportado en {detector.friendly_name}")

    def restart(self):
        print(f"[AUTO] Reinicio no soportado en {detector.friendly_name}")

    def lock(self):
        print(f"[AUTO] Bloqueo no soportado en {detector.friendly_name}")


class NotificationBackend:

    def notify(self, title, message):
        raise NotImplementedError

    @staticmethod
    def get_backend():
        if detector.is_windows:
            return _WindowsNotification()
        if detector.is_linux:
            return _LinuxNotification()
        if detector.is_macos:
            return _MacNotification()
        return _FallbackNotification()


class _WindowsNotification(NotificationBackend):

    def notify(self, title, message):
        try:
            from plyer import notification
            notification.notify(title=title, message=message, timeout=5)
        except ImportError:
            print(f"[NOTIFY] {title}: {message}")


class _LinuxNotification(NotificationBackend):

    def notify(self, title, message):
        import subprocess
        try:
            subprocess.Popen(["notify-send", title, message])
        except FileNotFoundError:
            print(f"[NOTIFY] {title}: {message}")


class _MacNotification(NotificationBackend):

    def notify(self, title, message):
        import subprocess
        script = f'display notification "{message}" with title "{title}"'
        subprocess.Popen(["osascript", "-e", script])


class _FallbackNotification(NotificationBackend):

    def notify(self, title, message):
        print(f"[NOTIFY] {title}: {message}")


def get_platform_automation():
    return AutomationBackend.get_backend()


def get_platform_notification():
    return NotificationBackend.get_backend()
