# JARVIS — Próximos Pasos

## Prioridad Alta

- [ ] **Integración continua (CI)**: GitHub Actions para lint + test automáticos
- [ ] **Face Swap funcional**: Completar `swapface_module.py` con pipeline completo
- [ ] **Enhance IA**: Pipeline de mejora de imágenes con modelos reales (ESRGAN, GFPGAN)
- [ ] **Plugins**: Sistema de plugins externos cargables desde `plugins/`
- [ ] **Docker**: Contenedor Docker multi-arquitectura (amd64, arm64)

## Prioridad Media

- [ ] **Tests unitarios**: Cubrir core, modules, ui con pytest
- [ ] **Tests de integración**: Flujo completo CLI + web + voz
- [ ] **Documentación API**: Mejorar `docs/api/API.md` con ejemplos
- [ ] **Instalador**: Script `install.sh` / `install.ps1` para deployment
- [ ] **Web UI v2**: Panel de administración, gráficas en tiempo real
- [ ] **FaceSwap**: Pipeline de video completo con seguimiento temporal

## Prioridad Baja

- [ ] **Internacionalización**: Soporte multi-idioma (en, pt, fr, de)
- [ ] **Módulo de respaldo**: Backup automático de configuración y memoria
- [ ] **Asistente por voz**: Diálogo bidireccional completo
- [ ] **Modo oscuro / claro**: Toggle en UI web y desktop
- [ ] **Tema personalizable**: Paletas de colores configurables

## Bugs Conocidos

- [ ] `voice.voice` causa `ModuleNotFoundError` si se importa desde directorio incorrecto
- [ ] numpy DLL rotas en ciertos entornos Windows (`ImportError: DLL load failed`)
- [ ] Los handlers vacíos en `system/` (power_manager, thermal_manager, etc.) causan warnings
