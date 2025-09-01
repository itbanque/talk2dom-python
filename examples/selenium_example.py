from selenium import webdriver

import time
from talk2dom.selenium import ActionChains
from talk2dom.client import Talk2DomClient

driver = webdriver.Chrome()
client = Talk2DomClient()

driver.get("https://python.org")

actions = ActionChains(driver, client)

actions.go("Type 'pycon' in the search box").go("Click the 'go' button")

time.sleep(2)
