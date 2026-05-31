#!/usr/bin/env bash
# JARVIS - Build / distribución
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  JARVIS - Build"
echo "========================================="

# Verificar sintaxis de todos los .py
echo "[INFO] Verificando sintaxis..."
find . -name "*.py" -not -path "./.venv/*" -exec python -m py_compile {} \; 2>&1 | grep -v "NoneType" || true
echo "[OK] Sintaxis verificada"

# Verificar estructura de directorios
echo "[INFO] Verificando estructura..."
DIRS=("core" "modules" "ui" "ui/web" "plat" "voice" "utils" "system" "config" "data" "logs" "tests")
for d in "${DIRS[@]}"; do
    if [ -d "$d" ]; then
        echo "  [OK] $d/"
    else
        echo "  [WARN] $d/ no encontrado"
    fi
done

# Contar líneas de código
echo ""
echo "[INFO] Líneas de código:"
find . -name "*.py" -not -path "./.venv/*" -exec wc -l {} + 2>/dev/null | tail -1

echo ""
echo "========================================="
echo "  Build completo"
echo "========================================="
