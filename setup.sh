#!/bin/bash
set -euo pipefail

echo "╔══════════════════════════════════════════════════╗"
echo "║   JOSAMICK UNIFIED — VERIFICACION PRE-VUELO     ║"
echo "╚══════════════════════════════════════════════════╝"

ERRORS=0

check() {
    local n=$1; shift
    echo -n "[${n}] $* ... "
}

ok()   { echo "OK"; }
fail() { echo "FALLO"; ERRORS=$((ERRORS+1)); }

# ─── 1. Docker ──────────────────────────────────────────────────────
check 1 "Docker instalado"
if command -v docker &>/dev/null; then ok; else fail; fi

# ─── 2. Docker Compose ──────────────────────────────────────────────
check 2 "Docker Compose"
if docker compose version &>/dev/null || docker-compose --version &>/dev/null; then ok; else fail; fi

# ─── 3. .env ────────────────────────────────────────────────────────
check 3 "Archivo .env"
if [ -f .env ]; then ok; else
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "CREADO DESDE .env.example"
    else
        fail
    fi
fi

# ─── 4. Directorios ─────────────────────────────────────────────────
check 4 "Directorios de servicio"
for d in c2_gateway brain_intelligence dashboard_ui auth_service email_service; do
    if [ ! -d "$d" ]; then echo "FALTA:$d"; ERRORS=$((ERRORS+1)); return 1; fi
done; ok

# ─── 5. Directorios de datos ────────────────────────────────────────
check 5 "Directorios de datos"
for d in data/users data/mail_logs data/forensics data/logs; do
    mkdir -p "$d"
done; ok

# ─── 6. Sintaxis Python ─────────────────────────────────────────────
check 6 "Sintaxis Python"
for f in c2_gateway/server.py brain_intelligence/runner.py dashboard_ui/server.py; do
    if [ -f "$f" ] && python3 -m py_compile "$f" 2>/dev/null; then
        :
    else
        echo "ERROR:$f"; ERRORS=$((ERRORS+1))
    fi
done; ok

# ─── 7. Puertos libres ──────────────────────────────────────────────
check 7 "Puertos disponibles"
for port_var in C2_PORT=9090 JOSAMICK_PORT=5001 KEXPLER_PORT=5002 AUTH_PORT=8001 EMAIL_PORT=8002; do
    port_name="${port_var%%=*}"
    port_num="${port_var##*=}"
    final_port="${!port_name:-$port_num}"
    if ss -tlnp "sport = :$final_port" 2>/dev/null | grep -q ":$final_port"; then
        echo "OCUPADO:$port_name($final_port)"; ERRORS=$((ERRORS+1))
    fi
done; ok

# ─── 8. Permisos Docker ─────────────────────────────────────────────
check 8 "Permisos Docker"
if docker info &>/dev/null; then ok; else fail; fi

echo ""
echo "╔══════════════════════════════════════════════════╗"
if [ "$ERRORS" -eq 0 ]; then
    echo "║  TODAS LAS VERIFICACIONES PASARON              ║"
    echo "║  Desplegando ecosistema...                     ║"
    echo "╚══════════════════════════════════════════════════╝"
    docker compose up -d --build
    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║  JOSAMICK UNIFIED — EN LINEA                    ║"
    echo "║  C2 Gateway:   http://localhost:${C2_PORT:-9090}    ║"
    echo "║  Brain:        http://localhost:${JOSAMICK_PORT:-5001}  ║"
    echo "║  Dashboard:    http://localhost:${KEXPLER_PORT:-5002}  ║"
    echo "║  Auth:         http://localhost:${AUTH_PORT:-8001}     ║"
    echo "║  Email:        http://localhost:${EMAIL_PORT:-8002}     ║"
    echo "╚══════════════════════════════════════════════════╝"
else
    echo "║  SE ENCONTRARON $ERRORS ERRORES                     ║"
    echo "║  Revisa las verificaciones fallidas e intenta de  ║"
    echo "║  nuevo.                                           ║"
    echo "╚══════════════════════════════════════════════════╝"
    exit 1
fi
