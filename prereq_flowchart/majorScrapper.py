from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import re
import time

class Course:
    credits: int
    title:str
    catalogTitle:str
    description:str
    inOr:bool #This is to indicate that the course has options
    required:bool
    def __init__(self,credits,title,catalogTitle,description,inOr,required):
        self.credits=credits
        self.title=title
        self.catalogTitle=catalogTitle
        self.description=description
        self.inOr=inOr
        self.required=required
    def getJSON(self):
        return{  "credits"      :self.credits,
                 "title"        :self.title,
                 "catalogTitle" :self.catalogTitle,
                 "description"  :self.description,
                 "inOr"         :self.inOr,
                 "required"     :self.required}


class Major:
    courses:[]
    minCredits:int
    name:str
    def __init__(self,courses,minCredits,name):
        self.courses=courses
        self.minCredits=minCredits
        self.name=name
    def getJSON(self):
        mappedCourses=list(map(lambda c:c.getJSON(),self.courses))
        return{"courses"   :mappedCourses,
               "minCredits":self.minCredits,
               "name"      :self.name}

def getMajorLinks():
    MAJOR_URL="https://onestop2.umn.edu/pcas/viewCatalogSearchResults.do?campusId=UMNTC&userDefinedSearch=true&keyworjds=&careerId=UGRD&programType=BACC"

    browser=webdriver.Firefox()
    browser.get(MAJOR_URL)
    browser.maximize_window()

    numberOfMajors=re.match("[0-9]*",browser.find_element(By.CLASS_NAME,"requirementshead").get_attribute("textContent")).group(0)
    majorLinks=browser.find_element(By.ID,"appTable").find_element(By.TAG_NAME,"tbody").find_elements(By.CLASS_NAME, "bold100")
    #Links to different majors

    majorJSONlinks=[]
    for i in range(int(numberOfMajors)):
        curMajor=majorLinks[i].find_element(By.TAG_NAME,"a").get_attribute('href')
        majorJSONlinks.append(curMajor)

    file=open("majorLinks.json","w")
    file.write(json.dumps(majorJSONlinks))
    file.close()
    browser.close()

def scrapeMajors():
    browser=webdriver.Firefox()
    browser.maximize_window()

    try:
        linkFile=open("majorLinks.json","r")
    except IOError:
        getMajorLinks()
        linkFile=open("majorLinks.json","r")

    majorLinks=json.loads(linkFile.read())
    majorCatalog=[]

    for i in range(len(majorLinks)):
        browser.get(majorLinks[i])
        majorName=browser.find_element(By.CLASS_NAME,"programtitle").get_attribute("textContent")

        minCredText=(browser.find_element(By.CLASS_NAME,"catalogList").find_elements(By.TAG_NAME,"li"))[2].get_attribute("textContent")
        minCred=re.search("[0-9]+",minCredText).group(0)

        classes=browser.find_elements(By.XPATH,"//a[@onclick]/..")
        courses=[]
        for j in range(len(classes)):
            attr=str(classes[j].find_element(By.TAG_NAME,"a").get_attribute("onclick"))
            classID=re.search("courseInfo_[0-9]*",attr)[0]
            courseInfo=' '.join(classes[j].get_attribute("textContent").split())

            courseDesc=browser.find_element(By.ID,classID).find_element(By.CLASS_NAME,"textField").get_attribute("textContent")
            credits=re.search("[0-9]+\.[0-9]+",courseInfo).group(0)
            catalogTitle=re.search("\w+ [0-9]+W*H*",courseInfo).group(0)
            title=re.search("\w+ [0-9]+W*H* - (.*) \(.*",courseInfo).group(0)
            inOr=re.search("or ",courseInfo) !=None
            required=re.search("· ",courseInfo) !=None

            courses.append(Course(credits,title,catalogTitle,courseDesc,inOr,required))
        majorCatalog.append(Major(courses,minCred,majorName))

    majorCatalogFile=open("majorCatalog.json","w")
    mappedCatalog=list(map(lambda m:m.getJSON(),majorCatalog))
    json.dump(mappedCatalog,majorCatalogFile,indent=6)
    majorCatalogFile.close()
    browser.close()

if __name__=="__main__":
    scrapeMajors()
