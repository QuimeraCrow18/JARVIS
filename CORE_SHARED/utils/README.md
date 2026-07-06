# Utilidades de JARVIS

## Scripts

| Archivo | Descripción |
|---------|-------------|
| `autoregistrar.py` | Escanea `modules/` y auto-genera imports en `main.py` |
| `auto_watcher.py` | Vigila cambios en `modules/` con watchdog y recarga módulos |
| `git_auto_sync.py` | Auto commit + push a GitHub con debounce de 10s |

## Uso

```bash
# Registrar módulos manualmente
python utils/autoregistrar.py

# Iniciar watcher de módulos (recarga automática)
python utils/auto_watcher.py &

# Auto-sync con GitHub (se inicia automáticamente desde main.py)
python utils/git_auto_sync.py
```

## Notas

- `autoregistrar.py` se ejecuta automáticamente al inicio de `main.py`
- `git_auto_sync.py` corre en un hilo daemon y hace commit de cambios cada 10s
- `auto_watcher.py` requiere el paquete `watchdog`
