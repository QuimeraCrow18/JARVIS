# =========================================
# JARVIS - PROCESS MANAGER
# =========================================

import psutil


class ProcessManager:

    def list_processes(self):

        print("\n=== PROCESOS ===")

        for process in psutil.process_iter(['pid', 'name']):

            try:
                print(process.info)

            except:
                pass