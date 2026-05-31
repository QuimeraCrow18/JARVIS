#!/usr/bin/env bash
# JARVIS - Script de instalación multi-plataforma
# Soporta: Linux, macOS, Windows (Git Bash / WSL)

set -e

echo "========================================="
echo "  JARVIS - Setup"
echo "========================================="

# Detectar Python
PYTHON=$(command -v python3 || command -v python || echo "")
if [ -z "$PYTHON" ]; then
    echo "[ERROR] Python no encontrado. Instala Python 3.10+"
    exit 1
fi

echo "[OK] Python: $($PYTHON --version)"

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "[INFO] Creando entorno virtual..."
    $PYTHON -m venv .venv
    echo "[OK] Entorno virtual creado"
fi

# Activar y instalar dependencias
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)  # Windows
        source .venv/Scripts/activate ;;
    *)                       # Linux/macOS
        source .venv/bin/activate ;;
esac

echo "[INFO] Instalando dependencias..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "[OK] Dependencias instaladas"

# Crear directorios necesarios
mkdir -p logs data/knowledge_base data/known_faces

echo ""
echo "========================================="
echo "  Setup completo"
echo "  Ejecuta: python main.py"
echo "========================================="
