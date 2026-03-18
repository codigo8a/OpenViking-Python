import requests
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import QDRANT_URL, QDRANT_COLLECTION
from logger import get_logger

logger = get_logger("memory")

class MemoryManager:
    def __init__(self):
        try:
            self.client = QdrantClient(url=QDRANT_URL)
            self._ensure_collection()
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self.client = None

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == QDRANT_COLLECTION for c in collections)
        if not exists:
            # Simple vector config for text snippets
            self.client.create_collection(
                collection_name=QDRANT_COLLECTION,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )
            logger.info(f"Created collection: {QDRANT_COLLECTION}")

    def save_memory(self, text: str):
        """Saves a text memory. In a real scenario, you'd use embeddings."""
        if not self.client: return
        try:
            # Placeholder for actual embedding logic
            # For now, we'll store metadata. Real RAG needs embeddings.
            logger.info(f"Saving memory: {text[:50]}...")
            # self.client.upsert(...) 
        except Exception as e:
            logger.error(f"Error saving memory: {e}")

    def search_memory(self, query: str):
        """Searches memory for relevant context."""
        if not self.client: return "Memory system offline."
        # Placeholder for search logic
        return "Relevant context would go here."

memory = MemoryManager()
