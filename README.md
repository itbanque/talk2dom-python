# Talk2Dom Python SDK

Minimal client SDK to call the Talk2Dom API. Synchronous and async APIs with tiny helpers for Playwright/Selenium.

## Install (dev)
```bash
pip install -e .
# optional
pip install ".[selenium]"
pip install ".[playwright]"

## Quiack Start
```python
from talk2dom import Talk2DomClient

client = Talk2DomClient(
  api_key="YOUR_API_KEY",
  endpoint="https://api.talk2dom.com",  # or your server
  project_id="default",
)

# sync example (HTML from anywhere; Selenium shown in examples/)
res = client.locate("click the primary login button", html="<html>...</html>", url="https://example.com")
print(res.selector_type, res.selector_value)
```

## Async (Playwright)
See examples/playwright_example.py.

## Environment variables
- T2D_API_KEY
- T2D_PROJECT_ID
- T2D_ENDPOINT (optional; defaults to https://api.talk2dom.itbanqye.com)
