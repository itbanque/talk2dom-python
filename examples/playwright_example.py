from playwright.sync_api import sync_playwright
from talk2dom.playwright import PageNavigator


def main():
    with sync_playwright() as p:
        # Launch Chromium browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        navigator = PageNavigator(page)

        # Navigate to python.org
        page.goto("https://www.python.org")

        navigator.go("Type 'pycon' in the search box")

        navigator.go("Click the 'go' button")

        # Wait for results to load
        page.wait_for_timeout(3000)

        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()
