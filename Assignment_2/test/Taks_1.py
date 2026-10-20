from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.amazon.in")

    failures = []

    # 1. Validate page title
    try:
        expect(page).to_have_title(
            "Online Shopping site in India: Shop Online for Mobiles, Books, Watches, Shoes and More - Amazon.in"
        )
        print("Page title: PASS")
    except AssertionError:
        failures.append("Page title validation failed")
        print("Page title: FAIL")

    # 2. Validate Amazon logo
    try:
        expect(page.locator("#nav-logo")).to_be_visible()
        print("Amazon logo: PASS")
    except AssertionError:
        failures.append("Amazon logo validation failed")
        print("Amazon logo: FAIL")

    # 3. Validate search textbox
    try:
        expect(page.locator("#twotabsearchtextbox")).to_be_visible()
        print("Search textbox: PASS")
    except AssertionError:
        failures.append("Search textbox validation failed")
        print("Search textbox: FAIL")

    # 4. Validate search button
    try:
        expect(page.locator("#nav-search-submit-button")).to_be_visible()
        print("Search button: PASS")
    except AssertionError:
        failures.append("Search button validation failed")
        print("Search button: FAIL")

    # 5. Validate navigation bar
    try:
        expect(page.locator("#nav-xshop")).to_be_visible()
        print("Navigation bar: PASS")
    except AssertionError:
        failures.append("Navigation bar validation failed")
        print("Navigation bar: FAIL")

    # Capture screenshot if any validation fails
    if failures:
        page.screenshot(path="amazon_failure.png")
        print("\nScreenshot saved as amazon_failure.png")

        print("\nValidation failures:")
        for failure in failures:
            print("-", failure)
    else:
        print("\nAll validations passed!")

    input("Press Enter to close the browser...")
    browser.close()