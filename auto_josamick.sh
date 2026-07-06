#!/bin/bash
echo "=========================================="
echo "  JOSAMICK ECOSYSTEM - ARRANQUE SEGURO"
echo "=========================================="
echo ""
echo "[OK] CORE_SHARED detectado"
echo "[OK] OceanicShield AES-256 listo"
echo ""
echo "Levantando JOSAMICK (IA) en puerto 5001..."
python JOSAMICK/server.py &
PID_JOSAMICK=$!
sleep 2

echo "Levantando KEXPLER (Red Social) en puerto 5002..."
python KEXPLER/server.py &
PID_KEXPLER=$!
sleep 2

echo ""
echo "=========================================="
echo "  ECOSISTEMA EN LINEA"
echo "  JOSAMICK  :5001 (PID $PID_JOSAMICK)"
echo "  KEXPLER   :5002 (PID $PID_KEXPLER)"
echo "=========================================="
echo "Presiona Ctrl+C para detener ambos nodos."

trap "echo ''; echo 'Deteniendo...'; kill $PID_JOSAMICK $PID_KEXPLER 2>/dev/null; echo 'Ecosistema detenido.'; exit 0" SIGINT SIGTERM

wait
