import time
import requests
from typing import Optional
from config import (
    GROQ_API_KEY, OPENROUTER_API_KEY, CEREBRAS_API_KEY,
    MAX_RETRIES, DEFAULT_COOLDOWN, SHORT_COOLDOWN
)
from logger import get_logger

logger = get_logger("llm_router")

class LLMRouter:
    def __init__(self):
        self.cooldowns = {
            "groq": 0,
            "openrouter": 0,
            "cerebras": 0
        }
        self.providers = [
            {"name": "groq", "url": "https://api.groq.com/openai/v1/chat/completions", "key": GROQ_API_KEY, "model": "llama3-70b-8192"},
            {"name": "cerebras", "url": "https://api.cerebras.ai/v1/chat/completions", "key": CEREBRAS_API_KEY, "model": "llama3.1-70b"},
            {"name": "openrouter", "url": "https://openrouter.ai/api/v1/chat/completions", "key": OPENROUTER_API_KEY, "model": "meta-llama/llama-3-70b-instruct"}
        ]

    def _is_on_cooldown(self, provider_name: str) -> bool:
        return time.time() < self.cooldowns.get(provider_name, 0)

    def _set_cooldown(self, provider_name: str, duration: int):
        self.cooldowns[provider_name] = time.time() + duration
        logger.warning(f"Provider {provider_name} put on cooldown for {duration}s")

    def _call_provider(self, provider: dict, prompt: str) -> Optional[str]:
        if not provider["key"]:
            return None

        headers = {
            "Authorization": f"Bearer {provider['key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": provider["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        try:
            response = requests.post(provider["url"], json=data, headers=headers, timeout=15)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            
            if response.status_code == 429:
                logger.error(f"Rate limit hit for {provider['name']}")
                self._set_cooldown(provider["name"], DEFAULT_COOLDOWN)
            else:
                logger.error(f"Error from {provider['name']}: {response.status_code} - {response.text}")
                self._set_cooldown(provider["name"], SHORT_COOLDOWN)
                
        except Exception as e:
            logger.error(f"Exception calling {provider['name']}: {str(e)}")
            self._set_cooldown(provider["name"], SHORT_COOLDOWN)
            
        return None

    def ask(self, prompt: str) -> str:
        for attempt in range(MAX_RETRIES):
            for provider in self.providers:
                if self._is_on_cooldown(provider["name"]):
                    continue
                
                logger.info(f"Attempting query with {provider['name']}...")
                result = self._call_provider(provider, prompt)
                
                if result:
                    logger.info(f"Success with {provider['name']}")
                    return result
            
            logger.warning(f"All providers failed on attempt {attempt + 1}. Waiting 2s...")
            time.sleep(2)

        return "ACTION: answer\nRESPONSE: Lo siento, todos los proveedores de LLM están caídos o en cooldown."

router = LLMRouter()
