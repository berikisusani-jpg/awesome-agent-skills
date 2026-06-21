class EthicalSentinel:
    def evaluate_action(self, action):
        if "delete" in action.lower(): return {"aligned": False, "reason": "Destructive"}
        return {"aligned": True}
    def get_sentinel_report(self): return "Sentinel: ACTIVE"
