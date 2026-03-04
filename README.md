# IA-Gen Backend

[![GitHub repo](https://img.shields.io/badge/GitHub-luisforni-blue?style=flat&logo=github)](https://github.com/luisforni/ia-gen-backend)
[![License](https://img.shields.io/badge/License-MIT-green)](#licencia)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi)

API REST construida con FastAPI para el servicio de chat generativo. Implementa streaming SSE y se conecta con Ollama para la inferencia LLM.

## Estructura

```
ia-gen-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── chat.py        # Endpoint /api/v1/chat (streaming SSE)
│   │       │   └── health.py      # Endpoint /api/v1/health
│   │       └── api.py             # Router principal
│   ├── services/
│   │   ├── ollama_service.py      # Cliente Ollama (streaming)
│   │   └── redis_service.py       # Cliente Redis
│   ├── schemas/
│   │   └── chat.py                # Validación de entrada/salida
│   ├── core/
│   │   ├── config.py              # Variables de entorno
│   │   └── rate_limiter.py        # Rate limiting (slowapi)
│   ├── config/
│   │   └── prompts.json           # System prompt del modelo
│   └── main.py                    # Aplicación FastAPI
├── requirements.txt
├── Dockerfile
└── .env
```

## Uso recomendado: Docker Compose

La forma recomendada de ejecutar el backend es a través de Docker Compose desde [ia-gen-infra](https://github.com/luisforni/ia-gen-infra).

## Desarrollo local (sin Docker)

### Requisitos

- Python 3.11+
- Ollama instalado y ejecutándose en `http://localhost:11434`
- Redis en `http://localhost:6379` (opcional, para rate limiting)

### 1. Clonar el repositorio

```bash
git clone https://github.com/luisforni/ia-gen-backend.git
cd ia-gen-backend
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

El archivo `.env` ya incluye los valores por defecto para desarrollo local:

```bash
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=llama3.2:1b
REDIS_URL=redis://localhost:6379/0
PORT=8000
```

### 4. Descargar el modelo en Ollama

```bash
ollama pull llama3.2:1b
```

#### Modelos disponibles

| Modelo                  | Tamaño  | Descripción                                             | Comando                                |
|-------------------------|---------|---------------------------------------------------------|----------------------------------------|
| `llama3.2:1b`           | ~1.3 GB | Llama 3.2 ultraligero, rápido, ideal para desarrollo    | `ollama pull llama3.2:1b`              |
| `llama3.2:3b`           | ~2.0 GB | Llama 3.2 equilibrado entre velocidad y calidad         | `ollama pull llama3.2:3b`              |
| `llama3.1:8b`           | ~4.7 GB | Llama 3.1 de alta calidad, requiere más RAM             | `ollama pull llama3.1:8b`              |
| `phi3:mini`             | ~2.2 GB | Phi-3 de Microsoft, muy eficiente                       | `ollama pull phi3:mini`                |
| `phi`                   | ~1.6 GB | Phi-2 de Microsoft, ligero                              | `ollama pull phi`                      |
| `mistral:7b`            | ~4.1 GB | Mistral 7B, buena calidad general                       | `ollama pull mistral:7b`               |
| `gemma2:2b`             | ~1.6 GB | Gemma 2 de Google, equilibrado                          | `ollama pull gemma2:2b`                |
| `gemma2:9b`             | ~5.5 GB | Gemma 2 de Google, alta calidad                         | `ollama pull gemma2:9b`                |
| `qwen2.5:3b`            | ~1.9 GB | Qwen 2.5 de Alibaba, muy capaz en su tamaño             | `ollama pull qwen2.5:3b`               |
| `deepseek-r1:7b`        | ~4.7 GB | DeepSeek R1, orientado a razonamiento                   | `ollama pull deepseek-r1:7b`           |
| `nomic-embed-text`      | ~274 MB | Solo embeddings, no para chat                           | `ollama pull nomic-embed-text`         |

> El catálogo completo está en [ollama.com/library](https://ollama.com/library).

Una vez descargado el modelo, actualiza `MODEL_NAME` en el archivo `.env`:

```bash
MODEL_NAME=llama3.2:1b
```

Con Docker Compose, cámbialo en `ia-gen-infra/docker-compose.yml` y reinicia el backend:

```bash
docker compose restart backend
```

### 5. Iniciar el servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

## Endpoints

### `POST /api/v1/chat`

Envía un mensaje y recibe la respuesta en streaming (SSE).

**Request:**
```json
{
  "messages": [
    { "role": "user", "content": "Hola, ¿cómo estás?" }
  ]
}
```

**Response** (stream SSE):
```
data: {"type": "text_delta", "text": "¡Hola"}
data: {"type": "text_delta", "text": "! Estoy"}
...
data: {"type": "message_delta", "content": "¡Hola! Estoy bien."}
```

### `GET /api/v1/health`

Verifica el estado de los servicios.

**Response:**
```json
{ "status": "healthy", "redis": true, "ollama": true }
```

## Variables de entorno

| Variable             | Default                     | Descripción                        |
|----------------------|-----------------------------|------------------------------------|
| `OLLAMA_HOST`        | `http://localhost:11434`    | URL del servidor Ollama            |
| `MODEL_NAME`         | `llama3.2:1b`               | Modelo LLM a usar                  |
| `REDIS_URL`          | `redis://localhost:6379/0`  | URL de Redis                       |
| `PORT`               | `8000`                      | Puerto del servidor                |
| `ALLOWED_ORIGINS`    | `http://localhost:3000`     | Orígenes CORS permitidos           |
| `RATE_LIMIT_ENABLED` | `True`                      | Activar rate limiting              |

## Cambiar el modelo LLM

### Con Docker Compose (recomendado)

```bash
# 1. Descargar el modelo en Ollama
docker exec ollama ollama pull deepseek-r1:7b

# 2. Cambiar MODEL_NAME en ia-gen-infra/docker-compose.yml
#    - MODEL_NAME=deepseek-r1:7b

# 3. Reiniciar el backend
docker compose restart backend
```

> El archivo `.env` del backend **no tiene efecto en Docker**: la variable `MODEL_NAME` del `docker-compose.yml` tiene prioridad. El `.env` solo aplica en desarrollo local sin Docker.

### En desarrollo local (sin Docker)

```bash
# 1. Descargar el modelo en Ollama
ollama pull deepseek-r1:7b

# 2. Cambiar MODEL_NAME en .env
#    MODEL_NAME=deepseek-r1:7b

# 3. Reiniciar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Personalizar el prompt del sistema

Edita `app/config/prompts.json`:

```json
{
  "system_prompt": "Eres un asistente útil y conciso."
}
```

## Repositorios relacionados

- **Frontend**: [ia-gen-frontend](https://github.com/luisforni/ia-gen-frontend)
- **Infraestructura**: [ia-gen-infra](https://github.com/luisforni/ia-gen-infra)

## Licencia

MIT
