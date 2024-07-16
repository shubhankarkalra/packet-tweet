from playwright.async_api import async_playwright, TimeoutError

class ScreenshotService:
    @staticmethod
    async def capture_screenshot(tweet_url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()
            await page.goto(tweet_url, wait_until="networkidle")
            
            try:
                # Wait for the tweet to load
                tweet_selector = '[data-testid="tweet"]'
                await page.wait_for_selector(tweet_selector, timeout=10000)
                
                # Get the bounding box of the tweet element
                tweet_element = await page.query_selector(tweet_selector)
                if tweet_element:
                    bbox = await tweet_element.bounding_box()
                    if bbox:
                        # Capture screenshot of the specific area
                        screenshot = await page.screenshot(clip=bbox)
                    else:
                        raise Exception("Couldn't get the bounding box of the tweet")
                else:
                    raise Exception("Tweet element not found")
            except TimeoutError:
                raise Exception("Timeout waiting for tweet to load")
            finally:
                await browser.close()
            
            return screenshot