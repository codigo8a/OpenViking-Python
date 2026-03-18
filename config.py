import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_config(key, default=None):
    """Retrieve config from Colab Secrets (userdata) or Environment Variables."""
    try:
        from google.colab import userdata
        return userdata.get(key)
    except (ImportError, Exception):
        return os.getenv(key, default)

# LLM API Keys
GROQ_API_KEY = get_config("GROQ_API_KEY")
OPENROUTER_API_KEY = get_config("OPENROUTER_API_KEY")
CEREBRAS_API_KEY = get_config("CEREBRAS_API_KEY")
OLLAMA_URL = get_config("OLLAMA_URL", "http://localhost:11434/v1/chat/completions")
OLLAMA_MODEL = get_config("OLLAMA_MODEL", "llama3:8b")

# Telegram Configuration
TELEGRAM_TOKEN = get_config("TELEGRAM_TOKEN")
NGROK_AUTHTOKEN = get_config("NGROK_AUTHTOKEN")
MCP_CONFIG_PATH = get_config("MCP_CONFIG_PATH", "mcp_config.json")

# Cloud Database (Firebase Firestore)
FIREBASE_PROJECT_ID = get_config("FIREBASE_PROJECT_ID")

# Agent Settings
MAX_RETRIES = 3
DEFAULT_COOLDOWN = 60  # seconds
SHORT_COOLDOWN = 15    # seconds
