import asyncio

class CinematicUXEngine:
    def __init__(self, speaker):
        self.speaker = speaker
        self.cinema_mode = True
        self.minimal_ui = False

    async def trigger_transition(self, mode_name):
        print(f"Friday: Orchestrating transition to '{mode_name}'...")
        await asyncio.sleep(0.8)
        return f"Transition to {mode_name} complete."

    def toggle_minimal_ui(self, enabled):
        """
        Reduces UI footprint for operational focus.
        """
        self.minimal_ui = enabled
        status = "ACTIVE" if enabled else "INACTIVE"
        print(f"Friday: Minimal UI Mode {status}.")
        return f"Minimal UI: {status}"

    def apply_visual_feedback(self, intensity):
        return f"Core UI Intensity set to {intensity * 100}%"
