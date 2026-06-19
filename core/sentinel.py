class EthicalSentinel:
    def __init__(self):
        self.rules = [
            "User Privacy is absolute.",
            "Autonomous actions must be reversible.",
            "Critical system changes require verification.",
            "Optimize for long-term user well-being."
        ]

    def evaluate_action(self, action_description):
        """
        Friday checks if an intended autonomous action aligns with its ethical sentinel rules.
        """
        print(f"Friday: Sentinel checking action - {action_description}")

        # Simulated alignment check
        if "delete" in action_description.lower() or "shutdown" in action_description.lower():
            return {"aligned": False, "reason": "Destructive actions require explicit confirmation per Sentinel Rule #3."}

        return {"aligned": True, "reason": "Action aligned with core Friday Ethics."}

    def get_sentinel_report(self):
        return f"Ethical Sentinel: ONLINE. {len(self.rules)} rules active."
