from selenium.webdriver.common.by import By
import re
import json
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException


def getMajorLinks():
    MAJOR_URL="https://onestop2.umn.edu/pcas/viewCatalogSearchResults.do?campusId=UMNTC&userDefinedSearch=true&keywords=&careerId=UGRD&programType=BACC"

    browser=webdriver.Firefox()
    browser.get(MAJOR_URL)
    browser.maximize_window()

    numberOfMajors=re.match("[0-9]*",browser.find_element(By.CLASS_NAME,"requirementshead").get_attribute("textContent")).group(0)
    majorLinks=browser.find_element(By.ID,"appTable").find_element(By.TAG_NAME,"tbody").find_elements(By.CLASS_NAME, "bold100")
    #Links to different majors

    majorJSONlinks=[]
    #Walk through major pages
    for i in range(int(numberOfMajors)):
        curMajor=majorLinks[i].find_element(By.TAG_NAME,"a").get_attribute('href')
        majorJSONlinks.append(curMajor)

    file=open("majorLinks.json","w")
    file.write(json.dumps(majorJSONlinks))
    file.close()
    browser.close()



def getMajorInfo():
    credElem=browser.find_element(By.CLASS_NAME,'catalogList')
    classElems=browser.find_elements(By.CLASS_NAME,"catText")
    for i in range(len(classElems)):
        #Plan is to filter and put into json, for now print
        print(classElems[i].get_attribute("textContent").strip())

