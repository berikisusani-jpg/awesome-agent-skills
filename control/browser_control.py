from playwright.sync_api import sync_playwright

class BrowserControl:
    def browse_to(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            # Add logic for further interaction
            browser.close()

    def search_web(self, query):
        url = f"https://www.google.com/search?q={query}"
        self.browse_to(url)
