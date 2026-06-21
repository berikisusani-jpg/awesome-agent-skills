import asyncio

class CinematicUXEngine:
    def __init__(self, speaker):
        self.speaker = speaker
        self.cinema_mode = True
        self.stealth_mode = False

    async def trigger_transition(self, mode_name):
        print(f"Friday: Transitioning to '{mode_name}' mode...")
        await asyncio.sleep(0.5)
        return f"Transition to {mode_name} complete."

    def toggle_stealth_mode(self, enabled):
        """
        Reduces console output and UI animations.
        """
        self.stealth_mode = enabled
        status = "ON" if enabled else "OFF"
        print(f"Friday: Stealth mode (reduced feedback) is now {status}.")
        return f"Stealth Mode: {status}"

    def apply_visual_feedback(self, intensity):
        return f"UI feedback intensity set to {intensity * 100}%"
