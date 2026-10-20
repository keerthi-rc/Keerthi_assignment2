
import pytest
from playwright.async_api import async_playwright, expect


# Static Dropdowns and Selected-Option Validation
@pytest.mark.asyncio
async def test_static_dropdown():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            executable_path="/usr/bin/google-chrome"
        )

        try:
            page = await browser.new_page()

            await page.goto(
                "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # The dropdown is inside the example iframe.
            frame = page.frame_locator("#iframeResult")
            dropdown = frame.locator("select")

            # Verify that the dropdown is visible.
            await expect(dropdown).to_be_visible()

            # Select an option by its visible label.
            await dropdown.select_option(label="Opel")

            # Validate the selected option.
            selected_option = dropdown.locator("option:checked")
            selected_text = await selected_option.text_content()

            assert selected_text is not None
            assert selected_text.strip() == "Opel", (
                f"Expected 'Opel', but got '{selected_text}'"
            )

            print("Selected option:", selected_text.strip())
            print("Dropdown selection validated successfully.")

            # Keep the browser open briefly to view the result.
            await page.wait_for_timeout(5000)

        except Exception as error:
            print(f"Test failed: {type(error).__name__}: {error}")
            raise

        finally:
            await browser.close()
