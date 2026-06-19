from database.supabase_client import SupabaseClient
from database.vector_store import VectorStore

class FridayMemory:
    def __init__(self):
        self.supabase = SupabaseClient()
        self.vector_store = VectorStore()

    def store_conversation(self, role: str, content: str):
        # Store in Supabase for persistence
        data = {"role": role, "content": content}
        self.supabase.insert_data("conversations", data)
        # Add to vector store for semantic search
        self.vector_store.add_memory(content, data)

    def retrieve_relevant_memories(self, query: str):
        return self.vector_store.search(query)

    def extract_and_store_facts(self, text: str):
        # Simplified fact extraction
        if "like" in text or "love" in text:
            self.vector_store.add_memory(text, {"category": "Personal"})
