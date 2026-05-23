# =========================================
# JARVIS - RESOURCE MONITOR
# =========================================

import psutil


class ResourceMonitor:

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_ram_usage(self):
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        return psutil.disk_usage('/').percent

    def show_resources(self):

        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()
        disk = self.get_disk_usage()

        print("\n=== RECURSOS ===")
        print(f"CPU: {cpu}%")
        print(f"RAM: {ram}%")
        print(f"DISCO: {disk}%")