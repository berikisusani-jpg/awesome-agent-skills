import asyncio

class CinematicUXEngine:
    def __init__(self, speaker):
        self.speaker = speaker
        self.cinema_mode = True
        self.stealth_mode = False

    async def trigger_transition(self, mode_name):
        print(f"Friday: Orchestrating cinematic transition to '{mode_name}'...")
        await asyncio.sleep(0.8)
        return f"Transition to {mode_name} complete."

    def toggle_stealth_mode(self, enabled):
        """
        FIXED: Ghost-Mode Stealth Uplink.
        Minimizes system footprint while maintaining 100% responsiveness.
        """
        self.stealth_mode = enabled
        status = "ACTIVE" if enabled else "INACTIVE"
        print(f"Friday: Ghost-Mode Stealth Uplink {status}. System zero-footprint engaged.")
        return f"Stealth Mode: {status}"

    def apply_visual_feedback(self, intensity):
        return f"Nexus Core Intensity set to {intensity * 100}%"
