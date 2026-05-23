# =========================================
# JARVIS AI SYSTEM
# startup.py
# =========================================

from core.kernel import JarvisKernel


def start_jarvis():

    print("================================")
    print("      JARVIS INITIALIZING       ")
    print("================================")

    kernel = JarvisKernel()

    kernel.boot()

    kernel.load_core_modules()

    kernel.show_loaded_modules()

    print("\nJarvis online.")