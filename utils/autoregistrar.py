import os
import re

MODULES_DIR = "modules"
MAIN_FILE = "main.py"

def get_module_names():
    return [f[:-3] for f in os.listdir(MODULES_DIR)
            if f.endswith(".py") and not f.startswith("__") and not f.startswith("test")]

def build_imports_block(mod_names):
    block = "# == AUTOLOADED MODULES START ==\n"
    for name in mod_names:
        block += f"from {MODULES_DIR}.{name} import *\n"
    block += "# == AUTOLOADED MODULES END ==\n"
    return block

def inject_autoloaded_modules_in_main():
    with open(MAIN_FILE, "r", encoding="utf-8") as f:
        src = f.read()

    mods = get_module_names()
    block = build_imports_block(mods)

    pat = re.compile(
        r"# == AUTOLOADED MODULES START ==[\s\S]*?# == AUTOLOADED MODULES END =="
    )
    if "# == AUTOLOADED MODULES START ==" in src:
        src = pat.sub(block, src)
    else:
        src = block + "\n" + src

    with open(MAIN_FILE, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"Autoregistro completado. Módulos importados: {', '.join(mods)}")

if __name__ == "__main__":
    inject_autoloaded_modules_in_main()