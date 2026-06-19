import numpy as np
from database.vector_store import VectorStore

class SubconsciousMind:
    def __init__(self):
        self.vector_store = VectorStore()
        self.active_patterns = []

    def surface_patterns(self, current_context):
        """
        Friday surfaces relevant 'subconscious' patterns without a direct query.
        """
        # We use a broad search to find clusters of relevant memories
        memories = self.vector_store.search(current_context, top_k=20)

        # Simulated pattern clustering logic
        patterns = [m.get("category") for m in memories if m.get("category")]
        unique_patterns = list(set(patterns))

        self.active_patterns = unique_patterns
        return unique_patterns

    def get_intuition(self):
        if "High Priority" in self.active_patterns:
            return "I have a strong intuition that we should prioritize the current task given past results."
        return "System intuition: Neutral. Proceed with caution."
