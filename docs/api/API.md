# JARVIS — API REST

## Base URL

```
http://<ip>:8080/api/
```

## Endpoints

### Estado del Sistema

**`GET /api/status`**

Respuesta:
```json
{
  "platform": {
    "friendly_name": "Windows 11",
    "system": "Windows",
    "machine": "AMD64",
    "python": "3.12.0",
    "is_desktop": true,
    "has_display": true
  },
  "memory": { "facts": 10, "preferences": 3, "conversations": 25 },
  "modules": ["voice", "media", "learning", "webremote", "knowledge"],
  "server_time": "2025-05-31T12:00:00"
}
```

**`GET /api/platform`**

```json
{
  "friendly_name": "Windows 11",
  "system": "Windows",
  "machine": "AMD64",
  "python": "3.12.0"
}
```

### Comandos

**`POST /api/command`**

Body:
```json
{ "command": "status" }
```

Respuesta:
```json
{ "command": "status", "result": "Módulos cargados: voice, media..." }
```

### Memoria

**`GET /api/memory`** — Lista todos los hechos aprendidos

**`POST /api/memory`** — Aprende un hecho nuevo

Body:
```json
{ "key": "color_favorito", "value": "azul" }
```

**`GET /api/conversations`** — Últimas 20 conversaciones

### Conocimiento

**`POST /api/knowledge/query`**

Body:
```json
{ "query": "inteligencia artificial" }
```

Respuesta:
```json
{
  "query": "inteligencia artificial",
  "results": [
    {
      "content": "...",
      "source": "url:https://...",
      "topic": "web/example.com",
      "score": 15
    }
  ]
}
```

**`POST /api/knowledge/absorb`**

Body (texto):
```json
{ "text": "contenido", "source": "web", "topic": "general" }
```

Body (URL):
```json
{ "url": "https://..." }
```

**`GET /api/knowledge/stats`**

```json
{ "total_absorbed": 42, "topics": 5, "sources": 3, "keywords_indexed": 120 }
```

**`GET /api/knowledge/topics`**

```json
["general", "web/example.com", "ia/python"]
```

**`POST /api/knowledge/search`**

Body:
```json
{ "topic": "general" }
```

### Backends IA

**`GET /api/backends`**

```json
{
  "ollama": { "available": true, "model": "llama3" },
  "openai": { "available": false }
}
```

## Códigos de Estado

| Código | Significado |
|--------|-------------|
| 200 | OK |
| 400 | Bad Request (parámetros faltantes) |
| 503 | Módulo no disponible |
| 404 | Endpoint no encontrado |
