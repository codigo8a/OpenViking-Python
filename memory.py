import uuid
import datetime
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import QDRANT_URL, QDRANT_COLLECTION
from logger import get_logger

logger = get_logger("memory")

class MemoryManager:
    def __init__(self):
        try:
            if QDRANT_URL:
                logger.info(f"Connecting to Qdrant at {QDRANT_URL}")
                self.client = QdrantClient(url=QDRANT_URL)
            else:
                logger.info("Using in-memory Qdrant (Colab-friendly)")
                self.client = QdrantClient(":memory:")
            self._ensure_collection()
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
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
        """Saves a text memory using a dummy vector (for simulation)."""
        if not self.client: return
        try:
            point_id = str(uuid.uuid4())
            timestamp = datetime.datetime.now().isoformat()
            
            logger.info(f"Saving memory ID {point_id}: {text[:50]}...")
            
            self.client.upsert(
                collection_name=QDRANT_COLLECTION,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=[0.0] * 384,  # Dummy vector
                        payload={"text": text, "timestamp": timestamp}
                    )
                ]
            )
        except Exception as e:
            logger.error(f"Error saving memory: {e}")

    def get_history(self, limit: int = 5):
        """Retrieves last recorded memories in Qdrant."""
        if not self.client: return "Memory system offline."
        try:
            points, _ = self.client.scroll(
                collection_name=QDRANT_COLLECTION,
                limit=100, # Get more to sort if needed
                with_payload=True,
                with_vectors=False
            )
            
            if not points:
                return "No hay recuerdos guardados todavía."
                
            # Sort by timestamp (descending)
            sorted_points = sorted(
                points, 
                key=lambda x: x.payload.get("timestamp", ""), 
                reverse=True
            )
            
            history_text = "📜 **Últimos recuerdos en Qdrant:**\n\n"
            for p in sorted_points[:limit]:
                text = p.payload.get("text", "Sin texto")
                time = p.payload.get("timestamp", "S/F").split("T")[1][:5]
                history_text += f"- [{time}] {text}\n"
                
            return history_text
        except Exception as e:
            logger.error(f"Error retrieving history: {e}")
            return f"Error al leer la memoria: {e}"

    def search_memory(self, query: str):
        """Retrieves the last relevant memories as context (simulated search)."""
        return self.get_history(limit=3)

memory = MemoryManager()
