# Talk2Dom Python SDK

![PyPI](https://img.shields.io/pypi/v/talk2dom)
[![PyPI Downloads](https://static.pepy.tech/badge/talk2dom)](https://pepy.tech/projects/talk2dom)
![Stars](https://img.shields.io/github/stars/itbanque/talk2dom-selenium?style=social)
![License](https://img.shields.io/github/license/itbanque/talk2dom-selenium)
![CI](https://github.com/itbanque/talk2dom-selenium/actions/workflows/test.yaml/badge.svg)

Minimal client SDK to call the Talk2Dom API.

## Install
```bash
pip install talk2dom
# optional
pip install "talk2dom[selenium]"
# or
pip install "talk2dom[playwright]"
```

```python
## Quiack Start
from talk2dom import Talk2DomClient

client = Talk2DomClient(
  api_key="YOUR_API_KEY",
  project_id="YOUR_PROJECT_ID",
)

# sync example
res = client.locate("click the primary login button", html="<html>...</html>", url="https://example.com")

# async exmaple
res = client.alocate("click the primary login button", html="<html>...</html>", url="https://example.com")
```

## Environment variables
- T2D_API_KEY
- T2D_PROJECT_ID
- T2D_ENDPOINT (optional; defaults to https://api.talk2dom.itbanque.com)

## Selenium ActionChains

```python
from selenium import webdriver

import time
from talk2dom.selenium import ActionChains

driver = webdriver.Chrome()

driver.get("https://python.org")

actions = ActionChains(driver)

actions\
    .go("Type 'pycon' in the search box")\
    .go("Click the 'go' button")

time.sleep(2)

```

## Playwright PageNavigator

```python
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


```