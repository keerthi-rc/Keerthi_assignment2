
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open Amazon and search for books
        await page.goto("https://www.amazon.in")
        await page.locator("#twotabsearchtextbox").fill("books")
        await page.locator("#nav-search-submit-button").click()

        # Locate products
        products = page.locator(
            "div[data-component-type='s-search-result']"
        )

        # Wait for products to appear
        await products.first.wait_for()

        # Count matching products
        count = await products.count()
        print("Number of matching products:", count)

        # Get all product titles
        titles = await products.locator("h2").all_inner_texts()

        print("\nAll product titles:")
        for title in titles:
            print(title)

        if count > 0:
            # First product title
            print("\nFirst product:", await products.first.locator("h2").inner_text())

            # Last product title
            print("Last product:", await products.last.locator("h2").inner_text())

            # Third product title
            if count >= 3:
                print("Third product:", await products.nth(2).locator("h2").inner_text())

            # Open the first product
            await products.first.locator("h2 a").click()
            await page.wait_for_load_state("domcontentloaded")

            print("\nOpened product:", await page.title())

        input("\nPress Enter to close the browser...")
        await browser.close()

asyncio.run(main())
