from selenium import webdriver
from selenium.webdriver.common.by import By
import majorinfo
import json
import re

browser=webdriver.Firefox()
browser.maximize_window()

linkFile=open("majorLinks.json","r")
majorLinks=json.loads(linkFile.read())


for i in range(3):
    browser.get(majorLinks[i])
    print(browser.find_element(By.CLASS_NAME,"programtitle").get_attribute("textContent"))

    classes=browser.find_elements(By.XPATH,"//a[@onclick]/..")
    for j in range(len(classes)):
        attr=str(classes[j].find_element(By.TAG_NAME,"a").get_attribute("onclick"))
        classID=re.search("courseInfo_[0-9]*",attr)[0]
        print(classes[j].get_attribute("textContent").split())
        print(browser.find_element(By.ID,classID).find_element(By.CLASS_NAME,"textField").get_attribute("textContent"))


browser.close()

