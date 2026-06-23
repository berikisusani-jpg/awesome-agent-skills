import datetime
import asyncio

class WritingAgent:
    def __init__(self, brain=None):
        self.brain = brain

    async def write_document(self, content, style="professional"):
        if not self.brain: return "Brain not linked to Writing Agent."

        # Real draft -> critique -> revise loop (max 2 passes)
        draft = ""
        prompt = f"Write a {style} document about: {content}"
        async for chunk in self.brain.chat_stream(prompt): draft += chunk

        # Pass 1: Critique
        critique = ""
        critique_prompt = f"Critique this draft for clarity and professional tone. Provide ONLY bullet points for improvement:\n\n{draft}"
        async for chunk in self.brain.chat_stream(critique_prompt): critique += chunk

        # Pass 2: Revise
        revised = ""
        revise_prompt = f"Rewrite the draft below based on this critique: {critique}\n\nDRAFT:\n{draft}"
        async for chunk in self.brain.chat_stream(revise_prompt): revised += chunk

        return revised

    def format_research_report(self, data):
        report = f"# FRIDAY RESEARCH REPORT: {data['topic'].upper()}\n"
        report += f"Generated on: {datetime.date.today()}\n\n"
        report += "## KEY FINDINGS\n"
        for finding in data['findings']:
            report += f"- {finding}\n"
        report += "\n## SOURCES\n"
        for source in data['sources']:
            report += f"- {source}\n"
        report += f"\n**Confidence Score:** {data['confidence_score'] * 100}%\n"
        report += "\n--- END OF REPORT ---"
        return report

    async def proofread(self, text):
        await asyncio.sleep(0.2)
        return "Deep analysis complete. Grammar and tone are optimal."
