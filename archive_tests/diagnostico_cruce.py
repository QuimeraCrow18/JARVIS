"""Diagnóstico: Cruce microfono_control.py <-> orchestrator.py"""
import os, sys, ast, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_history.log")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] [DIAG] {msg}\n")
    print(f"[{ts}] [DIAG] {msg}")

def extract_methods(filepath):
    with open(filepath, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    methods = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods[item.name] = item.lineno
    return methods

def extract_calls(filepath, target_class="MicrophoneControl"):
    with open(filepath, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == target_class:
                    calls.append((node.func.attr, node.lineno))
                if isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "_mic_control":
                    calls.append((node.func.attr, node.lineno))
    return calls

mic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "microphone_control.py")
orch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "core", "orchestrator.py")

print("=" * 60)
print("DIAGNÓSTICO DE CRUCE: microphone_control.py vs orchestrator.py")
print("=" * 60)

# 1. Métodos expuestos por MicrophoneControl
mic_methods = extract_methods(mic_path)
log(f"MicrophoneControl expone {len(mic_methods)} metodos: {list(mic_methods.keys())}")

# 2. Llamadas desde Orchestrator a MicrophoneControl
orch_calls = extract_calls(orch_path)
log(f"Orchestrator llama a MicrophoneControl en {len(orch_calls)} sitios")

# 3. Verificar invocaciones directas a self._mic_control.*
mic_attr_calls = []
with open(orch_path, encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if "_mic_control." in stripped and not stripped.startswith("#"):
        parts = stripped.split("_mic_control.")
        if len(parts) > 1:
            method_call = parts[1].split("(")[0]
            mic_attr_calls.append((method_call, i))

log(f"Accesos directos self._mic_control.*: {len(mic_attr_calls)}")
for method, line in mic_attr_calls:
    log(f"  LINEA {line}: _mic_control.{method}()")

# 4. Verificar cobertura de metodos
called_methods = set(m[0] for m in mic_attr_calls)
uncalled = [m for m in mic_methods if m not in called_methods and not m.startswith("_")]
log(f"Metodos publicos NO llamados por Orchestrator: {uncalled}")

# 5. Variables de entorno/config cruzadas
print()
log("Verificando config compartida...")
with open(mic_path, encoding="utf-8") as f:
    mic_src = f.read()
config_refs = [l.strip() for l in mic_src.split("\n") if "config" in l.lower() or "settings" in l.lower()]
log(f"Referencias a config en microphone_control: {len(config_refs)}")

# 6. Resumen final
print()
print("=" * 60)
log(f"RESUMEN: {len(mic_methods)} metodos en MicrophoneControl, {len(mic_attr_calls)} usados por Orchestrator, {len(uncalled)} sin usar")
print("=" * 60)
