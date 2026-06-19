class MemoryCompressor:
    def __init__(self, brain):
        self.brain = brain

    async def compress_memories(self, memory_list):
        """
        Friday distills a list of raw memories into a high-level 'Wisdom Token'.
        """
        print(f"Friday: Distilling {len(memory_list)} memories into Wisdom...")

        raw_text = " | ".join([m.get("content", "") for m in memory_list])

        prompt = f"""
        Analyze the following cluster of memories and distill them into a single 'Wisdom Token'.
        A Wisdom Token is a concise, high-level insight that preserves the essence of the data.
        DATA: {raw_text}
        """

        wisdom_token = ""
        async for chunk in self.brain.chat_stream(prompt):
            wisdom_token += chunk

        return wisdom_token

    def get_compression_ratio(self, original_count):
        # 100 memories -> 1 wisdom token
        return f"{original_count}:1"
