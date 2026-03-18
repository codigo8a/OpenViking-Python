import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import datetime
from config import get_config
from logger import get_logger

logger = get_logger("memory")

class MemoryManager:
    def __init__(self):
        try:
            # First check if firebase is already initialized
            project_id = get_config("FIREBASE_PROJECT_ID")
            
            if not firebase_admin._apps:
                if project_id:
                    logger.info(f"Initializing Firebase project: {project_id}")
                    # Use default credentials (local/Colab auth shell)
                    firebase_admin.initialize_app(options={'projectId': project_id})
                else:
                    logger.warning("No FIREBASE_PROJECT_ID. Memory will be in-memory list.")
                    self.db = None
                    self._fallback_history = []
                    return
            
            self.db = firestore.client()
            logger.info("Connected to Firebase Cloud Firestore.")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {e}")
            self.db = None
            self._fallback_history = []

    def save_memory(self, text: str):
        """Saves a text memory to Firestore."""
        if not self.db:
            timestamp = datetime.datetime.now().isoformat()
            self._fallback_history.append({"text": text, "timestamp": timestamp})
            return
            
        try:
            point_id = str(uuid.uuid4())
            timestamp = datetime.datetime.now() # Firestore handles datetimes
            
            doc_ref = self.db.collection('memories').document(point_id)
            doc_ref.set({
                "text": text,
                "timestamp": timestamp
            })
            logger.info(f"Saved to Cloud: {text[:50]}...")
        except Exception as e:
            logger.error(f"Error saving to Firestore: {e}")

    def get_history(self, limit: int = 5):
        """Retrieves last recorded memories in Firestore."""
        if not self.db:
            history_text = "📜 **Memoria Temporal (Local):**\n\n"
            for m in self._fallback_history[-limit:]:
                history_text += f"- {m['text']}\n"
            return history_text
            
        try:
            docs = self.db.collection('memories').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            history_text = "☁️ **Últimos recuerdos en Firebase:**\n\n"
            count = 0
            for doc in docs:
                count += 1
                data = doc.to_dict()
                text = data.get("text", "Sin texto")
                ts = data.get("timestamp")
                time_str = ts.strftime("%H:%M") if ts else "S/F"
                history_text += f"- [{time_str}] {text}\n"
                
            if count == 0:
                return "No hay recuerdos en la nube todavía."
                
            return history_text
        except Exception as e:
            logger.error(f"Error reading from Firestore: {e}")
            return "No se pudo leer de la nube. Revisa si Firestore está activo."

    def search_memory(self, query: str):
        return self.get_history(limit=3)

memory = MemoryManager()
