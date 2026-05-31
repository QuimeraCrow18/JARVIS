# Tests de JARVIS

## Estructura

```
tests/
├── unit/          # Pruebas unitarias (por módulo)
├── integration/   # Pruebas de integración (flujos completos)
├── e2e/           # Pruebas end-to-end (sistema completo)
└── README.md      # Este archivo
```

## Ejecutar Tests

```bash
# Todos los tests
make test

# Con pytest directamente
pytest tests/ -v --tb=short

# Tests unitarios específicos
pytest tests/unit/ -v

# Tests de integración
pytest tests/integration/ -v
```

## Convenciones

- Nombrar archivos: `test_<modulo>.py`
- Nombrar funciones: `test_<funcionalidad>`
- Usar `pytest` como framework
- Mockear dependencias externas (API calls, hardware)
- No depender de estado global compartido entre tests

## Cobertura Objetivo

- Core: 90%+
- Módulos principales: 70%+
- UI: 50%+
