#!/usr/bin/env bash
# JARVIS - Modo desarrollo con recarga automática
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

echo "[DEV] JARVIS - Modo desarrollo"
echo "[DEV] Log: logs/dev.log"
echo "[DEV] Iniciando..."

mkdir -p logs
python main.py --debug 2>&1 | tee logs/dev.log
