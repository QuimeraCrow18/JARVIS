#!/bin/bash
set -euo pipefail

echo "=============================================="
echo "  JOSAMICK MESH ENGINE - BOOTSTRAP UNIVERSAL"
echo "=============================================="

# --- Detectar SO ---
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "[i] Sistema: $OS / $ARCH"

# --- 1. Instalar dependencias base ---
install_deps() {
    echo "[1] Instalando dependencias del sistema..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y -qq docker.io docker-compose python3 python3-pip iptables curl openssl
    elif command -v yum &>/dev/null; then
        sudo yum install -y -q docker docker-compose python3 python3-pip iptables curl openssl
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm docker docker-compose python python-pip iptables curl openssl
    else
        echo "[!] Gestor de paquetes no detectado. Instala manualmente: docker, python3, iptables, openssl"
    fi
}

# --- 2. Generar claves mTLS para el nodo ---
setup_mtls() {
    echo "[2] Generando claves mTLS para este nodo..."
    mkdir -p .mesh/certs
    NODE_ID="nodo_$(hostname | md5sum | cut -c1-8)"
    echo "$NODE_ID" > .mesh/node_id

    openssl req -x509 -newkey rsa:4096 -keyout .mesh/certs/node.key \
        -out .mesh/certs/node.crt -days 3650 -nodes \
        -subj "/C=ES/ST=Mesh/O=JOSAMICK/CN=$NODE_ID" 2>/dev/null

    FINGERPRINT=$(openssl x509 -fingerprint -sha256 -in .mesh/certs/node.crt -noout | cut -d= -f2)
    echo "$FINGERPRINT" > .mesh/certs/fingerprint
    echo "[OK] Nodo: $NODE_ID"
    echo "[OK] Huella: $FINGERPRINT"
}

# --- 3. Registrar nodo en C2 ---
register_node() {
    echo "[3] Registrando nodo en el C2 Modular..."
    C2_URL="${C2_URL:-http://localhost:9090}"
    TOKEN="${SETUP_TOKEN:-}"

    if [ -z "$TOKEN" ]; then
        echo "[!] Variable SETUP_TOKEN no definida. Proporciona el token de un solo uso del 'Ser'."
        echo "    Uso: SETUP_TOKEN=<token> $0"
    else
        REG=$(curl -s -X POST "$C2_URL/mesh/register" \
            -H "Content-Type: application/json" \
            -d "{\"token\":\"$TOKEN\",\"node_id\":\"$(cat .mesh/node_id)\",\"fingerprint\":\"$(cat .mesh/certs/fingerprint)\"}")
        echo "[C2] Respuesta: $REG"
    fi
}

# --- 4. Desplegar contenedores ---
deploy_containers() {
    echo "[4] Desplegando contenedores Docker..."
    if [ ! -f .env ]; then
        cp .env.template .env
        echo "[i] Archivo .env creado desde .env.template. Revisa y ajusta valores."
    fi
    sudo docker-compose up -d --build
    echo "[OK] Contenedores desplegados."
}

install_deps
setup_mtls
register_node
deploy_containers

echo "=============================================="
echo "  NODO LISTO - JOSAMICK MESH ACTIVO"
echo "=============================================="
