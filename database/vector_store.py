import numpy as np
from sentence_transformers import SentenceTransformer
from database.supabase_client import SupabaseClient

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.supabase = SupabaseClient()

    def add_memory(self, text: str, meta: dict):
        embedding = self.model.encode(text).tolist()
        data = {
            "content": text,
            "metadata": meta,
            "embedding": embedding
        }
        self.supabase.insert_data("memories", data)

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode(query).tolist()
        # RPC call to Supabase pgvector function
        result = self.supabase.client.rpc('match_memories', {
            'query_embedding': query_embedding,
            'match_threshold': 0.5,
            'match_count': top_k,
        }).execute()
        return result.data
