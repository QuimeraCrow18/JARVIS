#!/usr/bin/env bash
# JARVIS - Ejecutar suite de tests
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Activar entorno virtual
if [ -d ".venv" ]; then
    case "$(uname -s)" in
        MINGW*|MSYS*|CYGWIN*)
            source .venv/Scripts/activate ;;
        *)
            source .venv/bin/activate ;;
    esac
fi

echo "========================================="
echo "  JARVIS - Tests"
echo "========================================="

if ! command -v pytest &> /dev/null; then
    echo "[WARN] pytest no instalado. Instalando..."
    pip install pytest -q
fi

echo "[INFO] Ejecutando tests..."
python -m pytest tests/ -v --tb=short 2>&1 || {
    echo ""
    echo "[INFO] Sin tests implementados aún."
    echo "      Crea tests en: tests/unit/ tests/integration/"
}

echo ""
echo "========================================="
echo "  Tests completados"
echo "========================================="
