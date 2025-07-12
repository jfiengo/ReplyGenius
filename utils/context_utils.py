import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from models import ContextItem

logger = logging.getLogger(__name__)

# Initialize sentence transformer for similarity search
embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_relevant_context(message: str, business_id: int, session, max_items: int = 3) -> str:
    """Get the most relevant context items for a message using similarity search"""
    try:
        # Get message embedding
        message_embedding = embeddings_model.encode(message)
        
        # Get all active context items for the business
        context_items = session.query(ContextItem).filter(
            ContextItem.business_id == business_id,
            ContextItem.is_active == True
        ).all()
        
        if not context_items:
            return ""
        
        # Calculate similarity scores
        similarities = []
        for item in context_items:
            if item.embedding is not None:
                similarity = np.dot(message_embedding, item.embedding) / (
                    np.linalg.norm(message_embedding) * np.linalg.norm(item.embedding)
                )
                similarities.append((item, similarity))
        
        # Sort by similarity and get top items
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_items = similarities[:max_items]
        
        # Format context
        context_text = ""
        for item, score in top_items:
            context_text += f"{item.title}:\n{item.content}\n\n"
        
        return context_text.strip()
        
    except Exception as e:
        logger.error(f"Error getting relevant context: {e}")
        return "" 