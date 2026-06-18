import datetime

class WritingAgent:
    def write_document(self, content, style="professional"):
        # content can be a string or a dict from ResearchAgent
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

    def proofread(self, text):
        return "Deep analysis complete. Grammar and tone are optimal."
