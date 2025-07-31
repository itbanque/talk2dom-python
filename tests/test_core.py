import pytest
from unittest.mock import MagicMock
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from talk2dom.core import (
    highlight_element,
)


@pytest.fixture
def mock_driver():
    driver = MagicMock(spec=WebDriver)
    element = MagicMock(spec=WebElement)
    element.get_attribute.return_value = (
        "<html><body><div id='main'>Content</div></body></html>"
    )
    driver.find_element.return_value = element
    driver.current_url = "http://example.com"
    return driver


def test_highlight_element():
    driver = MagicMock()
    element = MagicMock()
    element.get_attribute.return_value = ""
    highlight_element(driver, element, duration=0)
    assert driver.execute_script.call_count == 1
