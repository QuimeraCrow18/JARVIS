#!/bin/bash
set -euo pipefail

echo "=============================================="
echo "  JOSAMICK CLOUD - VERIFICACION PRE-VUELO"
echo "=============================================="

ERR=0

# --- 1. Verificar Docker ---
check_docker() {
    echo -n "[1] Docker disponible... "
    if command -v docker &>/dev/null; then
        echo "SI"
    else
        echo "NO"; ERR=1
    fi
}

# --- 2. Verificar docker-compose ---
check_compose() {
    echo -n "[2] Docker Compose disponible... "
    if docker compose version &>/dev/null || docker-compose --version &>/dev/null; then
        echo "SI"
    else
        echo "NO"; ERR=1
    fi
}

# --- 3. Verificar .env ---
check_env() {
    echo -n "[3] Archivo .env presente... "
    if [ -f .env ]; then
        echo "SI"
    else
        echo "NO (creando desde .env.template)"
        cp .env.template .env 2>/dev/null || echo "[!] No hay .env.template"
    fi
}

# --- 4. Verificar estructura de directorios ---
check_dirs() {
    echo -n "[4] Directorios modulares presentes... "
    for d in c2_modular brain_core frontend data; do
        if [ ! -d "$d" ]; then
            echo "FALTA: $d"; ERR=1
        fi
    done
    if [ "$ERR" -eq 0 ]; then echo "SI"; fi
}

# --- 5. Verificar requirements ---
check_reqs() {
    echo -n "[5] requirements.txt presente... "
    if [ -f requirements.txt ]; then
        echo "SI"
    else
        echo "NO"; ERR=1
    fi
}

# --- 6. Probar sintaxis Python ---
check_python() {
    echo -n "[6] Sintaxis Python de modulos... "
    for f in c2_modular/gateway.py; do
        if [ -f "$f" ]; then
            python3 -m py_compile "$f" 2>/dev/null && echo -n "." || { echo "ERROR:$f"; ERR=1; }
        fi
    done
    echo " OK"
}

# --- 7. Verificar puertos libres ---
check_ports() {
    echo -n "[7] Puertos disponibles... "
    for port in "${C2_PORT:-9090}" "${JOSAMICK_PORT:-5001}" "${KEXPLER_PORT:-5002}"; do
        if ss -tlnp "sport = :$port" 2>/dev/null | grep -q ":$port"; then
            echo "OCUPADO:$port"; ERR=1
        else
            echo -n "."
        fi
    done
    echo " OK"
}

# --- 8. Construir y lanzar ---
deploy() {
    echo ""
    echo "[8] Desplegando contenedores..."
    docker compose up -d --build
    echo ""
    echo "=============================================="
    echo "  JOSAMICK CLOUD - ECOSISTEMA EN LINEA"
    echo "=============================================="
    echo "  C2 Gateway:    http://localhost:${C2_PORT:-9090}"
    echo "  Brain Core:    http://localhost:${JOSAMICK_PORT:-5001}"
    echo "  Frontend:      http://localhost:${KEXPLER_PORT:-5002}"
    echo "=============================================="
    echo ""
    docker compose logs --tail=10
}

check_docker
check_compose
check_env
check_dirs
check_reqs
check_python
check_ports

if [ "$ERR" -eq 0 ]; then
    echo ""
    echo "[TODAS LAS VERIFICACIONES PASARON]"
    deploy
else
    echo ""
    echo "[ERRORES ENCONTRADOS] Corrige antes de desplegar."
    exit 1
fi
