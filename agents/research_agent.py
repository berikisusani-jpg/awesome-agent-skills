import requests
from bs4 import BeautifulSoup
import json
import asyncio

class ResearchAgent:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    async def search_and_summarize(self, brain, query):
        """
        Retiring fake implementation. Now calls the real DeepResearchSkill.
        """
        from skills.deep_research import DeepResearchSkill
        skill = DeepResearchSkill()
        return await skill.run(brain, {"topic": query})

    async def perform_deep_search(self, brain, topic):
        return await self.search_and_summarize(brain, topic)
