# JOSAMICK Ecosystem

Arquitectura de microservicios cloud-ready con 5 pilares operativos.

## Arquitectura

```
┌─────────────┐     ┌──────────────────┐
│  Usuarios   │────>│   c2_gateway     │ Puerto 9090 — Firewall, Auth, Mesh
└─────────────┘     └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │  Red Interna      │
                    │  172.28.0.0/16   │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
   ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
   │    brain    │   │  dashboard   │   │    auth      │
   │ inteligence │   │     ui       │   │   service    │
   │   :5001     │   │   :5002      │   │   :8001      │
   └─────────────┘   └──────────────┘   └──────┬───────┘
                                               │
                                        ┌──────▼───────┐
                                        │    email     │
                                        │   service    │
                                        │   :8002      │
                                        └──────────────┘
```

## Servicios

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| c2_gateway | 9090 | Centro de mando, firewall, autenticación |
| brain_intelligence | 5001 | Núcleo lógico de IA |
| dashboard_ui | 5002 | Interfaz web centralizada |
| auth_service | 8001 | Registro, login, aprobación de usuarios |
| email_service | 8002 | Notificaciones SMTP (@kexpler.com) |

## Flujo de Registro

```
Usuario → register.html → auth_service (Pendiente)
                                ↓
                    Alerta al C2 (forensic/alert)
                                ↓
                Arquitecto aprueba (POST /auth/approve)
                                ↓
                    email_service envía bienvenida
                                ↓
                Usuario inicia sesión → Dashboard
```

## Requisitos

- Docker + Docker Compose
- Git

## Despliegue Local

```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/josamick-ecosystem.git
cd josamick-ecosystem

# 2. Configurar entorno
cp .env.example .env
# Editar .env con tus claves y credenciales SMTP

# 3. Iniciar todo el ecosistema
docker compose up -d --build

# 4. Verificar estado
docker compose ps
docker compose logs --tail=20
```

## Despliegue en la Nube (Railway / Render / Fly.io)

### Opción 1: Railway.app

```bash
# 1. Subir a GitHub
git init
git add .
git commit -m "JOSAMICK Ecosystem v3.0"
git branch -M main
git remote add origin https://github.com/tuusuario/josamick-ecosystem.git
git push -u origin main

# 2. En Railway:
#    - "New Project" → "Deploy from GitHub"
#    - Seleccionar repositorio
#    - Railway detecta docker-compose.yml automáticamente
#    - Añadir variables de entorno en el dashboard
```

### Opción 2: Render

```bash
# Render requiere un servicio por contenedor:
# - c2_gateway:   Dockerfile en /c2_gateway,   puerto 9090
# - brain:        Dockerfile en /brain_intelligence, puerto 5001
# - dashboard:    Dockerfile en /dashboard_ui,  puerto 5002
# - auth:         Dockerfile en /auth_service,  puerto 8001
# - email:        Dockerfile en /email_service, puerto 8002
# Usar "Render Blueprint" con render.yaml para despliegue completo.
```

### Opción 3: VPS Manual

```bash
# En tu VPS (Ubuntu/Debian):
ssh usuario@tu-vps

sudo apt update && sudo apt install -y docker.io docker-compose
git clone https://github.com/tuusuario/josamick-ecosystem.git
cd josamick-ecosystem
cp .env.example .env
nano .env   # configurar claves y SMTP
docker compose up -d --build
```

## Variables de Entorno Clave

| Variable | Descripción |
|----------|-------------|
| C2_ADMIN_KEY | Clave maestra del C2 |
| SMTP_USER | Usuario SMTP (Brevo/SendGrid) |
| SMTP_PASS | Contraseña SMTP |
| FROM_EMAIL | Remitente (notificaciones@kexpler.com) |
| AUTH_JWT_SECRET | Secreto para tokens JWT |

## Persistencia

Todos los datos se almacenan en `./data/`:
- `data/users/auth.db` — Registros de usuarios
- `data/forensics/` — Dumps forenses cifrados
- `data/mail_logs/` — Logs de correos
- `data/logs/` — Logs del sistema

Estos datos sobreviven a `docker compose down`, actualizaciones y reinicios del servidor.

## Seguridad

- Red interna `mesh` (172.28.0.0/16) aislada del exterior
- Solo `c2_gateway` expone puertos al host
- Dashboard protegido por token contra `auth_service`
- Firewall automático (iptables) para nodos no whitelisted
- Circuit breaker en comunicaciones internas

## Licencia

JOSAMICK Core — Arquitecto Jose Crow Munoz
