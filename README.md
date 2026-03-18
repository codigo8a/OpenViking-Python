# 🏴‍☠️ OpenViking

**OpenViking** es un agente de IA autónomo diseñado para correr en Linux con acceso directo al sistema. A diferencia de otros agentes, no utiliza frameworks pesados como LangChain, apostando por una arquitectura modular, ligera y fácil de auditar.

## 🚀 Características

- **Arquitectura Modular:** Fácil de entender y extender.
- **Router de LLM Inteligente:** Soporte para Groq, OpenRouter y Cerebras.
- **Autocuración & Fallback:** Si un proveedor falla o llega al límite, cambia automáticamente.
- **Sistema de Cooldown:** Gestión inteligente de rate-limits (429) y errores.
- **Control Total de Sistema:** Ejecuta comandos bash, lee y escribe archivos.
- **Memoria Semántica:** Integración con Qdrant para persistencia de contexto.
- **Control Remoto:** Comunicación bidireccional vía Telegram.

## 🛠️ Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/openviking.git
   cd openviking
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar entorno:**
   Copia el archivo `.env.example` a `.env` y añade tus API Keys.
   ```bash
   cp .env.example .env
   ```

4. **Levantar servicios (Docker):**
   ```bash
   docker-compose up -d
   ```

## ☁️ Ejecutar en Google Colab

Si no quieres instalar nada localmente, puedes usar el notebook oficial:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/codigo8a/OpenViking-Python/blob/google-colab/OpenViking_Colab.ipynb)

1. Abre el enlace arriba.
2. Configura tus **Secrets** (icono 🔑) con `TELEGRAM_TOKEN`, `GROQ_API_KEY`, etc.
3. Ejecuta las celdas en orden.

## 🤖 Uso

### Modo CLI
Para interactuar directamente desde la terminal:
```bash
python agent.py
```

### Modo Telegram
Para habilitar el control remoto:
```bash
python telegram_bot.py
```

## ⚠️ Seguridad

> [!WARNING]
> **OpenViking tiene acceso a tu shell.** 
> Nunca lo ejecutes como usuario root. No le des acceso a sistemas de producción sensibles sin supervisión. Todos los comandos ejecutados se registran en `agent.log`.

## 📁 Estructura

- `agent.py`: Cerebro y loop principal.
- `llm_router.py`: Lógica de fallback y cooldown de proveedores.
- `tools.py`: Interacción con el sistema operativo.
- `memory.py`: Gestión de memoria a largo plazo.
- `planner.py`: Generador de estrategias y prompts.

## 📜 Licencia
MIT
