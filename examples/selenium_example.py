from selenium import webdriver

import time
from talk2dom.selenium import ActionChains

driver = webdriver.Chrome()

driver.get("https://python.org")

actions = ActionChains(driver)

actions.go("Type 'pycon' in the search box").go("Click the 'go' button")

time.sleep(2)
