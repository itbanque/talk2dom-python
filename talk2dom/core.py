import os
import time


from bs4 import BeautifulSoup


from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


from loguru import logger

import functools
import requests

DOMAIN = "https://api.talk2dom.itbanque.com"
API_KEY = os.environ.get("TALK2DOM_API_KEY")
PROJECT_ID = os.environ.get("TALK2DOM_PROJECT_ID")


def retry(
    exceptions: tuple = (Exception,),
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    logger_enabled: bool = True,
):
    """
    Retry decorator with exponential backoff.

    Args:
        exceptions: Tuple of exception classes to catch.
        max_attempts: Maximum number of retry attempts.
        delay: Initial delay between retries (in seconds).
        backoff: Multiplier applied to delay after each failure.
        logger_enabled: Whether to log retry attempts.

    Usage:
        @retry(max_attempts=5, delay=2)
        def unstable_operation():
            ...
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            current_delay = delay
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    if logger_enabled:
                        logger.warning(
                            f"[Retry] Attempt {attempt} failed: {e}. Retrying in {current_delay:.1f}s..."
                        )
                    time.sleep(current_delay)
                    current_delay *= backoff
                    attempt += 1

        return wrapper

    return decorator


def highlight_element(driver, element, duration=2):
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
    logger.debug(f"Highlighted element: {element}")


def get_html(element):
    html = (
        element.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
        if isinstance(element, WebDriver)
        else element.get_attribute("outerHTML")
    )
    soup = BeautifulSoup(html, "lxml")

    # remove unnecessary tags
    for tag in soup(["script", "style", "meta", "link"]):
        tag.decompose()

    html = soup.prettify()
    return html


# ------------------ Public API ------------------


def get_locator(
    element,
    description,
    conversation_history=None,
    url=None,
):
    """
    Get the locator for the element using LLM.
    :param element: The element to locate.
    :param description: The description of the element.
    :param model: The model to use for the LLM.
    :param model_provider: The model provider to use for the LLM.
    :param conversation_history: The conversation history to use for the LLM.
    :return: The locator type and value.
    """

    html = (
        element.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
        if isinstance(element, WebDriver)
        else element.get_attribute("outerHTML")
    )
    soup = BeautifulSoup(html, "lxml")

    # remove unnecessary tags
    for tag in soup(["script", "style", "meta", "link"]):
        tag.decompose()

    html = soup.prettify()
    logger.debug(
        f"Generating locator, instruction: {description}, HTML: {html[0:100]}..."
    )  # Log first 100 chars
    if not API_KEY:
        logger.error("Please provide TALK2DOM_API_KEY")
        raise Exception("Please provide TALK2DOM_API_KEY")
    if not PROJECT_ID:
        logger.error("Please provide TALK2DOM_PROJECT_ID")
        raise Exception("Please provide TALK2DOM_PROJECT_ID")
    endpoint = f"{DOMAIN}/api/v1/inference/locator?project_id={PROJECT_ID}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "url": url,
        "html": html,
        "user_instruction": description,
        "conversation_history": conversation_history,
    }

    response = requests.post(
        endpoint,
        json=body,
        headers=headers,
    )
    response.raise_for_status()
    response_obj = response.json()
    return response_obj["selector_type"], response_obj["selector_value"]


def get_element(
    driver,
    description,
    element=None,
    duration=None,
    conversation_history=None,
):
    """
    Get the element using LLM.
    :param driver: The WebDriver instance.
    :param description: The description of the element.
    :param element: The element to locate.
    :param model: The model to use for the LLM.
    :param model_provider: The model provider to use for the LLM.
    :param duration: The duration to highlight the element.
    :param conversation_history: The conversation history to use for the LLM.
    :return: The located element.
    """
    if element is None:
        selector_type, selector_value = get_locator(
            driver,
            description,
            conversation_history,
            url=driver.current_url,
        )
    else:
        selector_type, selector_value = get_locator(
            element,
            description,
            conversation_history,
            url=driver.current_url,
        )
    try:
        elem = driver.find_element(
            selector_type, selector_value
        )  # Ensure the page is loaded
    except Exception as e:
        raise e

    highlight_element(driver, elem, duration=duration)

    return elem
