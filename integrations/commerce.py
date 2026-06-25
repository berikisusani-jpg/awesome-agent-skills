from playwright.async_api import async_playwright
import datetime
from integrations.base import BaseIntegration

class CommerceIntegration(BaseIntegration):
    @property
    def name(self): return "Commerce"

    def available(self): return True

    async def execute(self, action, params=None):
        from control.browser_control import BrowserControl
        browser = BrowserControl()

        if action == "find_and_compare":
            item = params.get("item")
            print(f"Friday: Searching for {item} prices...")
            try:
                await browser.navigate(f"https://www.ebay.com/sch/i.html?_nkw={item.replace(' ', '+')}")
                # Real extraction logic
                page = browser.page
                # Wait for items to load
                await page.wait_for_selector(".s-item__price", timeout=5000)
                prices = await page.eval_on_selector_all(".s-item__price", "elements => elements.map(e => e.innerText)")
                titles = await page.eval_on_selector_all(".s-item__title", "elements => elements.map(e => e.innerText)")

                results = []
                for i in range(min(5, len(prices))):
                    results.append({"title": titles[i], "price": prices[i], "site": "eBay"})

                if not results:
                    return {"status": "error", "message": f"Could not find any items for {item}."}

                return {
                    "status": "success",
                    "message": f"Found {len(results)} results for {item} on eBay.",
                    "comparison": results
                }
            except Exception as e:
                return {"status": "error", "message": f"Commerce search failed: {e}"}

        if action == "checkout":
             # NO AUTO-APPROVE PATH: Hardcoded in ledger.py
             from core.ledger import get_ledger
             ledger = get_ledger()

             item = params.get("item")
             price = params.get("price")

             # Create action in ledger
             aid = ledger.queue_action("Commerce", "checkout", params, risk_level="high")

             # Wait for approval
             approved = await ledger.wait_for_approval(aid)
             if not approved:
                 return {"status": "rejected", "message": "Transaction was not approved by the user."}

             return {
                 "status": "success",
                 "message": f"Transaction of {price} for {item} completed (SANDBOX).",
                 "receipt": {
                     "item": item,
                     "total": price,
                     "approval_id": aid,
                     "timestamp": datetime.datetime.now().isoformat()
                 }
             }

        return {"status": "not_implemented"}
