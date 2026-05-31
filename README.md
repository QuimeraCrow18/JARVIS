# JARVIS - Sistema Inteligente de Protección

Asistente modular multi-plataforma con interfaz gráfica, procesamiento de medios, detección de fraudes, aprendizaje persistente y control remoto vía web.

## Características

- **Multi-plataforma**: Windows, Linux, macOS, Android (Termux), Raspberry Pi
- **Web Remote**: Interfaz web responsive desde cualquier dispositivo (móvil, tablet, smart TV)
- **API REST**: Control total via HTTP desde apps externas
- **Aprendizaje persistente**: JARVIS aprende y recuerda información entre sesiones
- **CLI interactivo** con comandos en español
- **Interfaz gráfica** moderna con `customtkinter` (monitoreo CPU/RAM, consola en vivo)
- **Procesamiento de medios**: detección de rostros, face swap, mejora de imagen, upscale 4K
- **Módulo de voz**: text-to-speech (TTS) y reconocimiento de voz
- **Automación**: abrir aplicaciones, sitios web, búsqueda de archivos, apagar/reiniciar PC
- **Detección de amenazas**: análisis de extorsión, suplantación de identidad, fraudes
- **Reconocimiento facial**: identificar rostros registrados
- **Auto-reparación** de dependencias al iniciar
- **Carga segura de módulos** con `SafeLoader` (los módulos que fallan no detienen el sistema)
- **Auto-sync con GitHub** mediante `watchdog`
- **Traductor de IA simbólica** experimental

## Estructura del Proyecto

```
JARVIS/
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias de Python
├── config/
│   ├── config.json            # Configuración general del sistema
│   └── logging.json           # Configuración de logging
├── core/
│   ├── auto_repair.py         # Verificación y reparación de dependencias
│   ├── config.py              # Constantes de configuración
│   ├── dependency_manager.py  # Gestor de instalación de paquetes
│   ├── error_manager.py       # Manejo centralizado de errores
│   ├── event_bus.py           # Bus de eventos (pub/sub)
│   ├── kernel.py              # Kernel principal del sistema
│   ├── logger.py              # Sistema de logging
│   ├── module_loader.py       # Cargador básico de módulos
│   ├── safe_loader.py         # Cargador seguro con manejo de fallos
│   └── utils.py               # Utilidades (decorador safe_method)
├── modules/
│   ├── voice_module.py        # Reconocimiento de voz y TTS
│   ├── media_module.py        # Procesamiento de imágenes y video
│   ├── enhance_module.py      # Mejora de imagen (filtros, upscale)
│   ├── automation_module.py   # Automatización del sistema
│   ├── memory_module.py       # Gestión de memoria RAM
│   ├── interaction_module.py  # Automatización de mouse/teclado
│   ├── fraud_detection_module.py
│   ├── extortion_analyzer.py
│   ├── identity_spoofing_detector.py
│   ├── threat_analyzer.py
│   ├── criminal_behavior_patterns.py
│   ├── context_video_vs_real_detector.py
│   ├── context_location_proximity_identity_detector_v2.py
│   ├── secure_communication.py
│   ├── swapface_module.py
│   ├── swapface_video_gender_blend.py
│   ├── render_module.py
│   ├── learning_module.py      # Sistema de memoria y aprendizaje persistente
│   ├── face_recognition_module.py  # Reconocimiento facial con DeepFace
│   ├── webremote_module.py     # Servidor web + API REST multi-plataforma
│   ├── app_module.py
│   ├── system_module.py
│   └── symbolic_ai/
│       └── translator.py      # Traductor de IA simbólica
├── ui/
│   ├── main_window.py         # Ventana principal (customtkinter)
│   ├── render_panel.py        # Panel de previsualización de video
│   ├── faces_panel.py         # Panel de selección de rostros
│   ├── media_ui.py            # Interfaz de medios
│   ├── web/                    # Interfaz web responsive
│   │   └── index.html          # UI multi-dispositivo
│   └── text_input.py          # Entrada de texto
├── plat/
│   ├── __init__.py
│   ├── detector.py             # Detección de plataforma (Win/Linux/Android...)
│   └── abstraction.py          # Abstracción multi-plataforma
├── voice/
│   ├── __init__.py            # VoiceSystem (TTS con pyttsx3)
│   └── voice.py               # Re-exporta VoiceSystem
├── utils/
│   ├── auto_watcher.py        # Vigilante de cambios en módulos
│   ├── autoregistrar.py       # Registro automático de módulos
│   └── git_auto_sync.py       # Sincronización automática con GitHub
├── system/
│   ├── resource_monitor.py    # Monitoreo de recursos del sistema
│   ├── system_manager.py      # Gestión del sistema
│   ├── proces_manager.py      # Gestión de procesos
│   └── ...                    # Placeholders para futuros módulos
├── data/
│   └── memory.json            # Almacenamiento de memoria persistente
├── logs/
│   └── jarvis.log             # Registro de eventos del sistema
└── tests/
    ├── unit/                  # Pruebas unitarias
    └── integration/           # Pruebas de integración
```

## Requisitos

- Python 3.10+
- Windows, Linux, macOS, Android (Termux), o Raspberry Pi

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/JARVIS.git
cd JARVIS

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

### Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `salir` / `exit` / `cerrar` | Cierra JARVIS |
| `status` | Muestra el estado de los módulos cargados |
| `reparar` | Ejecuta verificación y reparación de dependencias |
| `aprender <clave> = <valor>` | Enseña algo nuevo a JARVIS |
| `recuerda <clave>` | Recupera información aprendida |
| `olvida <clave>` | Olvida información específica |
| `que sabes` / `conocimientos` | Lista todo lo que JARVIS sabe |
| `conversaciones` / `historial` | Muestra interacciones recientes |
| `plataforma` / `platform` | Muestra información del sistema |
| `web on` / `web off` / `web url` | Control del servidor web remoto |
| `reconocer <imagen>` | Reconoce un rostro registrado |
| `registrar rostro <img> <nombre>` | Registra un rostro nuevo |
| `comparar rostros <a> <b>` | Compara dos imágenes |
| `detectar rostros <imagen>` | Detecta rostros en una imagen |
| `modifica rostro` | Face swap (en integración) |
| `mejora imagen` | Mejora de imagen con IA (en integración) |

### Web Remote (acceso multi-dispositivo)

```bash
# Iniciar servidor
python main.py
# En el CLI:
#   web on    - Inicia el servidor web
#   web url   - Muestra la URL para conectar
```

Luego desde cualquier dispositivo en la misma red (móvil, tablet, smart TV):
```
http://<ip>:8080
```

## Dependencias

- `psutil` - Monitoreo de CPU/RAM/disco
- `opencv-python` - Procesamiento de imágenes y video
- `customtkinter` - Interfaz gráfica moderna
- `pillow` - Manipulación de imágenes
- `numpy` - Cómputo numérico
- `pyttsx3` - Síntesis de voz (TTS)
- `SpeechRecognition` - Reconocimiento de voz
- `mediapipe` - Face swap y detección facial
- `deepface` - Análisis facial avanzado
- `watchdog` - Vigilancia de cambios en archivos
- `pyautogui` - Automatización de mouse/teclado
- `flask` - Servidor web API REST (opcional, usa http.server por defecto)

## Arquitectura

JARVIS utiliza una arquitectura modular multi-plataforma con carga segura:

1. **AutoRepair** verifica e instala dependencias faltantes al iniciar
2. **SafeLoader** carga cada módulo con manejo de excepciones individual
3. Si un módulo falla, se desactiva sin afectar al resto del sistema
4. **PlatformDetector** identifica el SO y activa funciones compatibles
5. **WebRemote** expone API REST + UI web responsive (accesible desde cualquier dispositivo)
6. **LearningModule** persiste conocimientos y conversaciones en `data/memory.json`
7. La interfaz gráfica (escritorio) se inicia en un hilo separado
8. **Git auto-sync** monitorea cambios y sincroniza automáticamente con GitHub

### Dispositivos soportados

| Dispositivo | Acceso | Funciones disponibles |
|------------|--------|----------------------|
| Windows/Linux/macOS | Local (CLI + GUI + Web) | Todas |
| Android (Termux) | CLI + Web | Voz, aprendizaje, cámara, SMS, GPS |
| Raspberry Pi | Local + Web | GPIO, sensores, automatización |
| Smart TV / iPad / iPhone | Web Remote | API REST, interfaz web responsive |
| Cualquier navegador | `http://<ip>:8080` | Chat, comandos, memoria |
