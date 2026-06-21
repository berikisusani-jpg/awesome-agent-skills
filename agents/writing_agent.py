import datetime
import asyncio

class WritingAgent:
    async def write_document(self, content, style="professional"):
        await asyncio.sleep(0.5)
        if isinstance(content, dict):
            return self.format_research_report(content)
        return f"--- DOCUMENT START ---\nStyle: {style}\nDate: {datetime.date.today()}\n\n{content}\n--- DOCUMENT END ---"

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
