#!/usr/bin/env python3
"""
JOSAMICK — Reporte de Estado de la Fortaleza (standalone)
Escaneo recursivo de josamick_core/, tools/, core/, modules/, ui/
Comparación con modules_registry.json
Generación de reporte de integración.
"""
import json
import os
import subprocess
import sys
import time

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPORTE_PATH = os.path.join(REPO_ROOT, "docs", "reporte_fortaleza.json")


def _py_files(raiz):
    result = []
    for root, dirs, files in os.walk(raiz):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(root, f), REPO_ROOT)
                result.append(rel)
    return sorted(result)


def _cargar_registry():
    path = os.path.join(REPO_ROOT, "josamick_core", "modules_registry.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"modulos": [], "ultimo_descubrimiento": 0, "cantidad": 0}


def _leer_requirements():
    path = os.path.join(REPO_ROOT, "requirements.txt")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def _chequear_lib(lib):
    try:
        import pkg_resources
        pkg_resources.get_distribution(lib)
        return True
    except Exception:
        return False
    try:
        if nombre in sys.modules:
            return True
        __import__(nombre)
        return True
    except ImportError:
        return False
    except Exception:
        return True


def generar_reporte():
    registry = _cargar_registry()
    modulos_registrados = set(registry.get("modulos", []))

    arbol = {
        "josamick_core": _py_files(os.path.join(REPO_ROOT, "josamick_core")),
        "tools": _py_files(os.path.join(REPO_ROOT, "tools")),
        "core": _py_files(os.path.join(REPO_ROOT, "core")),
        "modules": _py_files(os.path.join(REPO_ROOT, "modules")),
        "ui": _py_files(os.path.join(REPO_ROOT, "ui")),
    }

    modulos_en_disco = set()
    for f in arbol["core"] + arbol["modules"] + arbol["ui"] + arbol["josamick_core"] + arbol["tools"]:
        base = os.path.splitext(os.path.basename(f))[0]
        modulos_en_disco.add(base)

    integrados = sorted(modulos_registrados & modulos_en_disco)
    no_registrados = sorted(modulos_en_disco - modulos_registrados)
    solo_registro = sorted(modulos_registrados - modulos_en_disco)
    pipeline_traductor = [m for m in arbol["modules"] if "translator" in m]

    reqs = _leer_requirements()
    todas_libs = sorted(set(reqs))
    disponibilidad = {}
    for lib in todas_libs:
        try:
            nombre = lib.replace("-", "_")
            r = subprocess.run(
                [sys.executable, "-c", f"import {nombre}; print('ok')"],
                capture_output=True, timeout=10, cwd=REPO_ROOT,
            )
            disponibilidad[lib] = r.returncode == 0
        except Exception:
            disponibilidad[lib] = False

    instaladas = [lib for lib, ok in disponibilidad.items() if ok]
    pendientes = [lib for lib, ok in disponibilidad.items() if not ok]

    # Dependencias por plataforma (parseo simple del builder)
    builder_deps = {
        "android": ["python3", "jnius"],
        "windows": ["customtkinter", "PIL", "psutil", "cryptography", "textual"],
        "rpi": ["RPi.GPIO", "psutil", "cryptography"],
        "ios": ["pyobjus", "cryptography"],
        "iot": ["micropython", "cryptography"],
    }

    reporte = {
        "timestamp": time.time(),
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "resumen": {
            "modulos_en_registro": len(modulos_registrados),
            "modulos_en_disco": len(modulos_en_disco),
            "modulos_integrados": len(integrados),
            "modulos_no_registrados": len(no_registrados),
            "modulos_solo_en_registro": len(solo_registro),
            "dependencias_instaladas": len(instaladas),
            "dependencias_pendientes": len(pendientes),
        },
        "arbol_directorios": {k: v for k, v in arbol.items()},
        "modulos_integrados": integrados,
        "modulos_no_registrados": no_registrados,
        "modulos_solo_en_registro": solo_registro,
        "pipeline_traductor": pipeline_traductor,
        "dependencias": {
            "instaladas": instaladas,
            "pendientes": pendientes,
            "por_plataforma": builder_deps,
        },
    }

    os.makedirs(os.path.dirname(REPORTE_PATH), exist_ok=True)
    with open(REPORTE_PATH, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=4, ensure_ascii=False)

    # Salida legible
    sep = "=" * 62
    print(f"""
{sep}
 INFORME DE ESTADO DE LA FORTALEZA --- JOSAMICK
{sep}
  Fecha: {reporte['fecha']}
""")

    for dirname, archivos in arbol.items():
        print(f"  {dirname}/  ({len(archivos)} archivos)")

    print(f"""
{sep}
 1. MODULOS INTEGRADOS CON EXITO ({len(integrados)})
{sep}""")
    for m in integrados:
        print(f"     [OK] {m}")

    print(f"""
{sep}
 2. MODULOS EN PROCESO DE DESPLIEGUE --- PIPELINE TRADUCTOR
{sep}""")
    for m in pipeline_traductor:
        print(f"     [>>] {m}")
    print("""
     modules/translator/          -> Motor de traduccion (texto)
     modules/translator_voice/    -> Voz-a-voz con diarizacion + sintesis
       voice_diarizer.py          -> Perfilado genero/edad (F0+F1)
       voice_synthesizer.py       -> TTS con perfil (edge-tts/pyttsx3)
       audio_hooker.py            -> Captura WASAPI loopback
       audio_mixer.py             -> Balance original<->traduccion
       overlay_controller.py      -> FAB + Event-Driven (On-Demand)
    """)

    print(f"{sep}\n 3. DEPENDENCIAS PENDIENTES ({len(pendientes)})\n{sep}")
    for lib in pendientes if pendientes else ["(ninguna)"]:
        print(f"     [MISS] {lib}")
    print()

    for plat, libs in builder_deps.items():
        ok_list = [l for l in libs if l in instaladas]
        print(f"     {plat}: {len(ok_list)}/{len(libs)}")
        for lib in libs:
            d = "[OK]" if lib in instaladas else "[MISS]"
            print(f"       {d} {lib}")

    print(f"""
{sep}
 RESUMEN
{sep}
  Modulos integrados:              {len(integrados)}
  Modulos en disco no registrados: {len(no_registrados)}
  Modulos solo en registro:        {len(solo_registro)}
  Dependencias instaladas:         {len(instaladas)}
  Dependencias pendientes:         {len(pendientes)}
{sep}""")
    if not pendientes:
        print("  VEREDICTO: FORTALEZA OPERATIVA - Lista para compilacion multi-plataforma")
    else:
        print(f"  VEREDICTO: FORTALEZA EN CONSTRUCCION - {len(pendientes)} dependencia(s) pendiente(s)")

    print(f"\n  Reporte JSON: {REPORTE_PATH}\n")
    return reporte


if __name__ == "__main__":
    generar_reporte()
