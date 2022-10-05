from selenium.webdriver.common.by import By
import re
import json
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

file=open("majorRequirements.json","w")

MAJOR_URL="https://onestop2.umn.edu/pcas/viewCatalogSearchResults.do?campusId=UMNTC&userDefinedSearch=true&keywords=&careerId=UGRD&programType=BACC"

browser=webdriver.Firefox()
browser.get(MAJOR_URL)
browser.maximize_window()

numberOfMajors=re.match("[0-9]*",browser.find_element(By.CLASS_NAME,"requirementshead").get_attribute("textContent")).group(0)
majorLinks=browser.find_element(By.ID,"appTable").find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"a")
#Links to different majors


def getMajorInfo():
    credElem=browser.find_element(By.CLASS_NAME,'catalogList')
    classElems=browser.find_elements(By.CLASS_NAME,"catText")
    for i in range(len(classElems)):
        #Plan is to filter and put into json, for now print
        print(classElems[i].get_attribute("textContent").strip())


#Walk through major pages
for i in range(int(numberOfMajors)):
    try:
        print("Getting "+majorLinks[2*i].get_attribute("textContent"))
        curMajor=majorLinks[2*i].get_attribute('href')
        browser.get(curMajor)
        getMajorInfo()
        browser.back()
    except StaleElementReferenceException:
        #I believe server is rejecting the connection to prevent excess traffic.
        #Not sure how to fix this, for now hoping to do enough work to create a 
        #significant delay.

        #print("Stale!")
        continue
