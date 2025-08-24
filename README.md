# Talk2Dom Python SDK

Minimal client SDK to call the Talk2Dom API.

## Install
```bash
pip install talk2dom
# optional
pip install "talk2dom[selenium]"
pip install "talk2dom[playwright]"

## Quiack Start
```python
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
from selenium.webdriver.common.keys import Keys

from talk2dom.selenium import ActionChains
from talk2dom.client import Talk2DomClient

driver = webdriver.Chrome()
client = Talk2DomClient()

driver.get("https://python.org")

actions = ActionChains(driver, client)
actions.predict_element("Find the Search box").click().send_keys("pycon").send_keys(
    Keys.ENTER
).perform()

```