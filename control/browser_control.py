from playwright.async_api import async_playwright
import asyncio
import time

class BrowserControl:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.audit_log = "browser_control_audit.log"

    def _log_action(self, action, params):
        with open(self.audit_log, "a") as f:
            f.write(f"{time.ctime()} | Action: {action} | Params: {params}\n")

    async def start(self, headless=False):
        self._log_action("start_browser", {"headless": headless})
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def navigate(self, url):
        if not self.page: await self.start()
        self._log_action("navigate", {"url": url})
        await self.page.goto(url)
        return f"Navigated to {url}"

    async def click_element(self, selector, confirm=False):
        if not confirm: return "Permission denied."
        self._log_action("click_element", {"selector": selector})
        await self.page.click(selector)
        return f"Clicked {selector}"

    async def type_text(self, selector, text, confirm=False):
        if not confirm: return "Permission denied."
        self._log_action("type_text", {"selector": selector, "text": text})
        await self.page.fill(selector, text)
        return f"Typed into {selector}"

    async def extract_page_text(self):
        return await self.page.inner_text("body")

    async def take_screenshot(self, path="browser_shot.png"):
        await self.page.screenshot(path=path)
        return path

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
