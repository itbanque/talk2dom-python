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
