import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from talk2dom.client import Talk2DomClient


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
