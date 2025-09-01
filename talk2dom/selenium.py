import time
from loguru import logger

try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.common.action_chains import (
        ActionChains as SeleniumActionChains,
    )
except ImportError:
    raise ImportError(
        "selenium is not installed, please run `pip install talk2dom[selenium]`"
    )

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


def go(
    driver: WebDriver,
    instruction: str,
    client: Talk2DomClient,
    element: WebElement = None,
):
    html = _get_html(driver, element)
    res = client.locate(instruction, html=html, url=driver.current_url)
    by, value = res.selector_type, res.selector_value
    if not value:
        logger.warning(f"Locator value {value} not for {by}")
        return
    action_type, action_value = res.action_type, res.action_value
    el = driver.find_element(by, value)
    _highlight_element(driver, el)
    if action_type == "click":
        el.click()
    elif action_type == "type":
        if not action_value:
            logger.warning(
                f"Action value {action_value} not provided for {action_type}"
            )
            return
        el.clear()
        el.send_keys(action_value)
    else:
        logger.warning(f"action type: {action_type} is not supported")


class ActionChains(SeleniumActionChains):
    def __init__(
        self,
        driver: WebDriver,
        client: Talk2DomClient = None,
        duration: int = 250,
        devices=None,
    ):
        super().__init__(driver, duration=duration, devices=devices)
        self.client = client if client else Talk2DomClient()

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

    def go(self, instruction: str, use_last_element=False):
        html = (
            _get_html(self._driver, self._last_element)
            if use_last_element
            else _get_html(self._driver)
        )
        res = self.client.locate(instruction, html=html, url=self._driver.current_url)
        by, value = res.selector_type, res.selector_value
        if not value:
            logger.warning(f"Locator value {value} not for {by}")
            return self
        action_type, action_value = res.action_type, res.action_value
        el = self._driver.find_element(by, value)
        _highlight_element(self._driver, el)
        self.move_to_element(el)
        if action_type == "click":
            el.click()
        elif action_type == "type":
            if not action_value:
                logger.warning(
                    f"Action value {action_value} not provided for {action_type}"
                )
                return self
            el.clear()
            el.send_keys(action_value)
        else:
            logger.warning(f"action type: {action_type} is not supported")
        return self
