
import pytest
from playwright.async_api import (
    async_playwright,
    expect,
    TimeoutError as PlaywrightTimeoutError
)


@pytest.mark.asyncio
async def test_handle_timeouts():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path="/usr/bin/google-chrome"
        )

        try:
            page = await browser.new_page()

            # 1. Set the default action timeout to 10 seconds
            page.set_default_timeout(10000)

            # Open Google
            await page.goto(
                "https://www.google.com",
                wait_until="domcontentloaded",
                timeout=30000
            )

            # 2. Wait for a valid element using a custom timeout
            search_box = page.locator("textarea[name='q']")

            await expect(search_box).to_be_visible(timeout=5000)
            print("Success: Google search box is visible.")

            # 3. Deliberately locate a non-existent element
            missing_element = page.locator(
                "#element-that-does-not-exist"
            )

            try:
                await missing_element.wait_for(
                    state="visible",
                    timeout=3000
                )

                print("Element unexpectedly became visible.")

            except PlaywrightTimeoutError:
                # 4. Handle the expected timeout gracefully
                print(
                    "Timeout handled: The missing element "
                    "was not visible within 3 seconds."
                )

            # Confirm the test can continue
            await expect(search_box).to_be_visible()
            print("Test completed successfully.")

        except Exception as error:
            # 5. Report unexpected failures and preserve test failure
            print(
                f"Unexpected failure: "
                f"{type(error).__name__}: {error}"
            )
            raise

        finally:
            await browser.close()
