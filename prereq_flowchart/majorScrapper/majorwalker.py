from selenium import webdriver
from selenium.webdriver.common.by import By
import majorinfo
import json

browser=webdriver.Firefox()
browser.maximize_window()

linkFile=open("majorLinks.json","r")
majorLinks=json.loads(linkFile.read())


for i in range(len(majorLinks)):
    browser.get(majorLinks[i])
    print(browser.find_element(By.CLASS_NAME,"programtitle").get_attribute("textContent"))

    credElem=browser.find_element(By.CLASS_NAME,'catalogList')
    classElems=browser.find_elements(By.CLASS_NAME,"catText")
    print(classElems[i].get_attribute("textContent").strip())


