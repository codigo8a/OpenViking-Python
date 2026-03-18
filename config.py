import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# LLM API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Vector Database (Qdrant)
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "openviking_memory")

# Agent Settings
MAX_RETRIES = 3
DEFAULT_COOLDOWN = 60  # seconds
SHORT_COOLDOWN = 15    # seconds
