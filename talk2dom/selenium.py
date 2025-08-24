import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains as SeleniumActionChains

from .client import Talk2DomClient


def _get_html(driver: WebDriver, element: WebElement = None):
    if element:
        return element.get_attribute("outerHTML")
    return driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")


def _highlight_element(driver: WebDriver, element: WebElement, duration=2):
    style = (
        "box-shadow: 0 0 10px 3px rgba(255, 0, 0, 0.7);"
        "outline: 2px solid red;"
        "background-color: rgba(255, 230, 200, 0.3);"
        "transition: all 0.2s ease-in-out;"
    )
    original_style = element.get_attribute("style")
    driver.execute_script(f"arguments[0].setAttribute('style', '{style}')", element)
    if duration:
        time.sleep(duration)
        driver.execute_script(
            f"arguments[0].setAttribute('style', `{original_style}`)", element
        )


def get_element(
    driver: WebDriver,
    instruction: str,
    client: Talk2DomClient,
    element: WebElement = None,
):
    html = _get_html(driver, element)
    res = client.locate(instruction, html=html, url=driver.current_url)
    by, value = res.selector_type, res.selector_value
    el = driver.find_element(by, value)
    _highlight_element(driver, el)
    return el


def click(
    driver: WebDriver,
    instruction: str,
    client: Talk2DomClient,
    element: WebElement = None,
):
    html = _get_html(driver, element)
    res = client.locate(instruction, html=html, url=driver.current_url)
    by, value = res.selector_type, res.selector_value
    el = driver.find_element(by, value)
    _highlight_element(driver, el)
    el.click()


def send_keys(
    driver: WebDriver,
    instruction: str,
    text: str,
    client: Talk2DomClient,
    element: WebElement = None,
):
    html = _get_html(driver, element)
    res = client.locate(instruction, html=html, url=driver.current_url)
    by, value = res.selector_type, res.selector_value
    el = driver.find_element(by, value)
    _highlight_element(driver, el)
    el.clear()
    el.send_keys(text)


class ActionChains(SeleniumActionChains):

    def __init__(
        self,
        driver: WebDriver,
        client: Talk2DomClient,
        duration: int = 250,
        devices=None,
    ):
        super().__init__(driver, duration=duration, devices=devices)
        self.client = client
        self._last_element: WebElement | None = None

    def predict_element(self, instruction: str) -> SeleniumActionChains:
        html = _get_html(self._driver, self._last_element)
        res = self.client.locate(instruction, html=html, url=self._driver.current_url)
        by, value = res.selector_type, res.selector_value
        el = self._driver.find_element(by, value)
        _highlight_element(self._driver, el)
        self.move_to_element(el)
        return self

    def move_to_element(self, to_element: WebElement) -> SeleniumActionChains:
        """Moving the mouse to the middle of an element.

        :Args:
         - to_element: The WebElement to move to.
        """

        self._last_element = to_element
        self.w3c_actions.pointer_action.move_to(to_element)
        self.w3c_actions.key_action.pause()

        return self

    @property
    def current_element(self):
        return self._last_element
