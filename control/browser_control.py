from playwright.async_api import async_playwright
import asyncio
import time
import datetime
import os
from config.settings import WORKSPACE_ROOT
from core.ledger import get_ledger

class BrowserControl:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.audit_log = "browser_control_audit.log"
        self.ledger = get_ledger()

    def _log_action(self, action, params):
        logging.getLogger("FridayControl").info({
            "component": "BrowserControl",
            "action": action,
            "params": params
        })

    async def _get_screenshot_receipt(self):
        shot_path = os.path.join(WORKSPACE_ROOT, f"browser_receipt_{int(time.time())}.png")
        await self.page.screenshot(path=shot_path)
        return {
            "type": "screenshot",
            "data": shot_path,
            "timestamp": datetime.datetime.now().isoformat()
        }

    async def _gate(self, action, params, risk_level="medium"):
        action_id = self.ledger.queue_action("BrowserControl", action, params, risk_level=risk_level)
        if await self.ledger.wait_for_approval(action_id):
            return True
        return False

    async def start(self, headless=False):
        self._log_action("start_browser", {"headless": headless})
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def navigate(self, url):
        if not self.page: await self.start()
        if not await self._gate("navigate", {"url": url}, risk_level="low"):
            return {"status": "error", "message": "Action rejected by user."}
        self._log_action("navigate", {"url": url})
        await self.page.goto(url)
        return {
            "status": "success",
            "message": f"Navigated to {url}",
            "receipt": await self._get_screenshot_receipt()
        }

    async def click_element(self, selector):
        if not await self._gate("click_element", {"selector": selector}):
            return {"status": "error", "message": "Action rejected by user."}
        self._log_action("click_element", {"selector": selector})
        await self.page.click(selector)
        return {
            "status": "success",
            "message": f"Clicked {selector}",
            "receipt": await self._get_screenshot_receipt()
        }

    async def type_text(self, selector, text):
        if not await self._gate("type_text", {"selector": selector, "text": text}):
            return {"status": "error", "message": "Action rejected by user."}
        self._log_action("type_text", {"selector": selector, "text": text})
        await self.page.fill(selector, text)
        return {
            "status": "success",
            "message": f"Typed into {selector}",
            "receipt": await self._get_screenshot_receipt()
        }

    async def close(self):
        if self.browser: await self.browser.close()
        if self.playwright: await self.playwright.stop()
