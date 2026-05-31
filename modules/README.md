# Módulos de JARVIS

## Estructura

```
modules/
├── ai_backends.py              # Interfaz multi-IA (Ollama, OpenAI, Anthropic, Gemini)
├── app_module.py               # Lanzador de aplicaciones
├── automation_module.py        # Automatización del sistema
├── criminal_behavior_patterns.py   # Análisis de patrones delictivos
├── enhance_module.py           # Mejora de imágenes
├── extortion_analyzer.py       # Detección de intentos de extorsión
├── face_recognition_module.py  # Reconocimiento facial con DeepFace
├── fraud_detection_module.py   # Detección de fraudes en llamadas/SMS
├── identity_spoofing_detector.py   # Detección de suplantación de identidad
├── interaction_module.py       # Automatización de entrada (mouse/teclado)
├── knowledge_engine.py         # Motor de conocimiento infinito
├── learning_module.py          # Memoria persistente (hechos, preferencias)
├── media_module.py             # Procesamiento de imágenes y video
├── memory_module.py            # Gestión de memoria RAM
├── optimizer_module.py         # Optimización del sistema
├── render_module.py            # Utilidades de renderizado
├── secure_communication.py     # Comunicación cifrada (Fernet)
├── swapface_module.py          # Face swap con MediaPipe
├── swapface_video_gender_blend.py   # Mezcla de género facial
├── system_module.py            # Operaciones del sistema
├── threat_analyzer.py          # Puntuación de amenazas
├── voice_module.py             # Módulo de entrada/salida de voz
├── webremote_module.py         # Servidor web + API REST
├── context_location_proximity_identity_detector_v2.py  # Detección contextual
├── context_video_vs_real_detector.py   # Discriminación video/real
└── symbolic_ai/
    └── translator.py           # Traductor de IA simbólica
```

## Convenciones

- Cada módulo debe tener un método `init()` o `__init__` que acepte referencias del sistema
- Usar `@safe_method` de `core.utils` para métodos que no deben romper el sistema
- Los módulos se cargan via `SafeLoader` en `main.py`
- Si un módulo falla al cargar, se desactiva sin afectar al resto

## Crear un Nuevo Módulo

1. Crear archivo en `modules/<nombre>.py`
2. La clase debe tener al menos `__init__(self)` 
3. Registrar en `main.py` con `loader.load_module("modules.<nombre>")`
4. Ejecutar `python utils/autoregistrar.py` para registro automático
