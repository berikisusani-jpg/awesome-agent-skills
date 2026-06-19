from playwright.async_api import async_playwright
import asyncio

class BrowserControl:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self, headless=False):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def navigate(self, url):
        if not self.page: await self.start()
        await self.page.goto(url)
        return f"Navigated to {url}"

    async def click_element(self, selector):
        await self.page.click(selector)
        return f"Clicked {selector}"

    async def type_text(self, selector, text):
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
