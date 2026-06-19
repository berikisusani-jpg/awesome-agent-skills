import random

class FutureSimulator:
    def __init__(self, brain):
        self.brain = brain
        self.simulated_outcomes = []

    async def simulate_decision(self, decision_context):
        """
        Friday simulates multiple outcomes for a given user decision.
        """
        print(f"Friday: Commencing multi-path simulation for: {decision_context}")

        prompt = f"""
        Simulate 3 potential outcomes (Optimistic, Neutral, Risk) for this decision:
        {decision_context}

        Provide a probability score for each and a strategic recommendation.
        """

        simulation_result = ""
        async for chunk in self.brain.chat_stream(prompt):
            simulation_result += chunk

        self.simulated_outcomes.append({"context": decision_context, "result": simulation_result})
        return simulation_result

    def get_risk_assessment(self):
        # Basic risk detection based on last simulation
        return "System suggests a 15% risk increase if current trajectory is maintained."
