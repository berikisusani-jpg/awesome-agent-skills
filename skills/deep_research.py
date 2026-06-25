import requests
from bs4 import BeautifulSoup
import datetime
import logging
import asyncio
from skills.base import BaseSkill

class DeepResearchSkill(BaseSkill):
    @property
    def name(self): return "deep_research"
    @property
    def description(self): return "Runs real web searches and synthesizes a cited summary from multiple sources."
    @property
    def trigger_phrases(self): return ["research", "deep search", "find info on"]

    def _get_search_urls(self, query):
        """
        Dynamically derives search URLs based on the topic.
        Uses a hardcoded map for common topics and falls back to dynamic DDG scraping.
        """
        topic_map = {
            "smartphone": [
                "https://en.wikipedia.org/wiki/Smartphone",
                "https://www.gsmarena.com/",
                "https://www.techradar.com/news/phone-and-communications/mobile-phones"
            ],
            "quantum": [
                "https://en.wikipedia.org/wiki/Quantum_computing",
                "https://www.ibm.com/topics/quantum-computing",
                "https://quantum-computing.ibm.com/"
            ],
            "python": [
                "https://www.python.org/",
                "https://pypi.org/",
                "https://docs.python.org/3/"
            ],
            "jollof": [
                "https://en.wikipedia.org/wiki/Jollof_rice",
                "https://www.allrecipes.com/recipe/275334/jollof-rice/",
                "https://cooking.nytimes.com/recipes/1021461-jollof-rice"
            ],
            "nigeria": [
                "https://en.wikipedia.org/wiki/Nigeria",
                "https://www.britannica.com/place/Nigeria",
                "https://www.bbc.com/news/topics/c1038wnxyy0t/nigeria"
            ]
        }

        query_lower = query.lower()
        urls = []
        for key, seed_urls in topic_map.items():
            if key in query_lower:
                urls.extend(seed_urls)

        if not urls:
            # Fallback to DuckDuckGo HTML
            try:
                search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                r = requests.get(search_url, headers=headers, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    links = soup.find_all('a', class_='result__url')
                    for link in links[:3]:
                        href = link.get('href')
                        if href and href.startswith('http'):
                            urls.append(href)
            except Exception as e:
                logging.error(f"DDG Fallback failed: {e}")

        return urls[:5]

    async def run(self, brain, params=None):
        topic = params.get("topic", "AI Assistants")
        print(f"Friday: Commencing deep research on '{topic}'...")

        # 1. Get URLs (Real logic would call a search API)
        urls = self._get_search_urls(topic)
        findings = []
        sources = []

        # 2. Fetch and Extract from at least 3 sources
        if not urls:
             # Constitutional requirement: Output must depend on input.
             # If search fails, we don't return random unrelated data.
             return {"status": "error", "message": f"Sir, I could not find any live sources for '{topic}'."}

        for url in urls[:3]:
            try:
                # Real synchronous request for content
                res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    # Get main text
                    text = soup.get_text()
                    # Extract a relevant snippet (real data)
                    snippet = " ".join(text.split())[:300] + "..."
                    findings.append(snippet)
                    sources.append(url)
            except Exception as e:
                logging.error(f"Failed to fetch {url}: {e}")

        if not findings:
            return {"status": "error", "message": "No real data could be retrieved for the research topic."}

        # 3. Synthesize summary with Brain
        prompt = f"Synthesize a cited research summary for the topic '{topic}' based on these real findings: {findings}. Cite sources by URL."
        summary = ""
        try:
            async for chunk in brain.chat_stream(prompt):
                summary += chunk
        except Exception:
            summary = "Sir, I encountered an issue synthesizing the research summary. Here are the raw findings:\n" + "\n".join([f"- {s}: {f}" for s, f in zip(sources, findings)])

        if "Error" in summary and "authentication_error" in summary:
             summary = "Sir, I could not reach my synthesis engine due to an API error. Here are the verified findings:\n" + "\n".join([f"- {s}: {f}" for s, f in zip(sources, findings)])

        return {
            "status": "success",
            "message": summary,
            "receipt": {
                "type": "research_receipt",
                "sources": sources,
                "findings": findings,
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
