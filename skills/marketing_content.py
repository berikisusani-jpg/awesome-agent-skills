import datetime
import logging
from skills.base import BaseSkill
from skills.deep_research import DeepResearchSkill

class MarketingContentSkill(BaseSkill):
    @property
    def name(self): return "marketing_content"
    @property
    def description(self): return "Generates labeled draft marketing content and competitive research."
    @property
    def trigger_phrases(self): return ["marketing content", "social media posts", "write ad copy"]

    async def run(self, brain, params=None):
        product = params.get("product", "AI Assistant")
        include_research = params.get("include_research", False)

        print(f"Friday: Commencing marketing content generation for '{product}'...")

        research_context = ""
        sources = []
        if include_research:
            research_skill = DeepResearchSkill()
            res = await research_skill.run(brain, {"topic": f"competitors for {product}"})
            if res["status"] == "success":
                research_context = res["message"]
                sources = res["receipt"]["sources"]

        # 1. Draft Content
        prompt = (f"Act as a professional marketer. Generate the following content for '{product}':\n"
                  f"1. A short blog post outline.\n"
                  f"2. Three social media captions.\n"
                  f"3. One ad copy variant.\n\n"
                  f"CONTEXT FROM RESEARCH (if any):\n{research_context}\n\n"
                  f"LABEL all content clearly as AI-generated drafts.")

        drafts = ""
        try:
            async for chunk in brain.chat_stream(prompt):
                drafts += chunk
        except Exception:
             drafts = "Sir, I encountered an issue generating the drafts. Please check the logs."

        if "Error" in drafts and "authentication_error" in drafts:
             drafts = (f"Sir, API access for drafting is limited. Here is a generic draft for human review:\n"
                       f"- Social Caption: Introducing {product}! Your next favorite tool. #AI\n"
                       f"- Ad variant: Experience the future with {product}. Sign up today.\n"
                       f"[LABEL: AI-GENERATED DRAFT]")

        full_message = f"--- COMPETITIVE RESEARCH ---\n"
        if sources:
            full_message += f"Found via real search: {', '.join(sources)}\n\n"
            full_message += f"{research_context}\n\n"
        else:
            full_message += "No real-time competitive data retrieved.\n\n"

        full_message += f"--- MARKETING DRAFTS (FOR HUMAN REVIEW) ---\n\n{drafts}"

        return {
            "status": "success",
            "message": full_message,
            "receipt": {
                "type": "marketing_receipt",
                "product": product,
                "research_performed": include_research,
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
