import time
from loguru import logger

try:
    from playwright.sync_api import Page, Locator
except ImportError:
    raise ImportError(
        "playwright is not installed, please run `pip install playwright` and `playwright install`"
    )

from .client import Talk2DomClient
from .utils import clean_html
from .exceptions import ElementNotFoundError


# ---------- Utilities ----------
def _get_html(page: Page, element: Locator | None = None) -> str:
    if element is not None:
        # outerHTML of the first matching element
        html = element.evaluate("el => el.outerHTML")
    else:
        html = page.locator("body").evaluate("el => el.outerHTML")
    return clean_html(html)


def _highlight_element(page: Page, element: Locator, duration: float = 2.0):
    style = (
        "box-shadow: 0 0 10px 3px rgba(255, 0, 0, 0.7);"
        "outline: 2px solid red;"
        "background-color: rgba(255, 230, 200, 0.3);"
        "transition: all 0.2s ease-in-out;"
    )

    page.evaluate(
        """([el, s, dur]) => {
            const prev = el.getAttribute('style') || '';
            el.setAttribute('style', s);
            setTimeout(() => { el.setAttribute('style', prev); }, Math.max(0, dur*1000));
        }""",
        [element.element_handle(), style, duration],
    )
    if duration:
        time.sleep(duration)


def _by_to_playwright_selector(selector_type: str, value: str) -> str:
    st = (selector_type or "").lower()
    if st in ("css selector", "css"):
        return value
    if st == "id":
        return f"#{value}"
    if st == "xpath":
        return f"xpath={value}"
    if st == "name":
        return f'[name="{value}"]'
    if st == "class name":
        cls = ".".join(value.strip().split())
        return f".{cls}"
    if st == "tag name":
        return value
    if st == "link text":
        return f'text="{value}"'
    if st == "partial link text":
        return f"text={value}"
    return value


def _find_locator(
    page: Page, selector_type: str, selector_value: str, timeout_ms: int = 10000
) -> Locator:
    if not selector_value:
        raise ElementNotFoundError("Element not found")
    sel = _by_to_playwright_selector(selector_type, selector_value)
    loc = page.locator(sel).first
    try:
        loc.wait_for(state="visible", timeout=timeout_ms)
    except Exception:
        loc.wait_for(state="attached", timeout=timeout_ms)
    return loc


# --------- PageNavigator Class ----------
class PageNavigator:
    def __init__(
        self, page: Page, client: Talk2DomClient = None, highlight: bool = True
    ):
        self.page = page
        self.client = client if client else Talk2DomClient()
        self.highlight = highlight

    def get_element(self, instruction: str, element: Locator | None = None) -> Locator:
        html = _get_html(self.page, element)
        res = self.client.locate(instruction, html=html, url=self.page.url)
        by, value = res.selector_type, res.selector_value
        loc = _find_locator(self.page, by, value)
        if self.highlight:
            _highlight_element(self.page, loc)
        return loc

    def wait_for(
        self, instruction: str, element: Locator = None, timeout: int = 10000
    ) -> Locator:
        html = _get_html(self.page, element)
        res = self.client.locate(instruction, html=html, url=self.page.url)
        by, value = res.selector_type, res.selector_value
        sel = _by_to_playwright_selector(by, value)
        self.page.wait_for_selector(sel, timeout=timeout)
        loc = self.page.locator(sel).first
        if self.highlight:
            _highlight_element(self.page, loc)
        return loc

    def click(self, instruction: str, element: Locator | None = None):
        html = _get_html(self.page, element)
        res = self.client.locate(instruction, html=html, url=self.page.url)
        by, value = res.selector_type, res.selector_value
        loc = _find_locator(self.page, by, value)
        if self.highlight:
            _highlight_element(self.page, loc)
        loc.click()

    def send_keys(self, instruction: str, text: str, element: Locator | None = None):
        html = _get_html(self.page, element)
        res = self.client.locate(instruction, html=html, url=self.page.url)
        by, value = res.selector_type, res.selector_value
        loc = _find_locator(self.page, by, value)
        if self.highlight:
            _highlight_element(self.page, loc)
        try:
            loc.fill("")
        except Exception:
            pass
        loc.type(text)

    def go(self, instruction: str, element: Locator | None = None):
        html = _get_html(self.page, element)
        res = self.client.locate(instruction, html=html, url=self.page.url)
        by, value = res.selector_type, res.selector_value
        action_type, action_value = res.action_type, res.action_value
        loc = _find_locator(self.page, by, value)
        if self.highlight:
            _highlight_element(self.page, loc)
        if action_type == "click":
            loc.click()
        elif action_type == "type":
            if not action_value:
                logger.warning(
                    f"Action value {action_value} not provided for {action_type}"
                )
                return
            try:
                loc.fill("")
            except Exception:
                pass
            loc.type(action_value)
        else:
            logger.warning(f"action type: {action_type} is not supported")
